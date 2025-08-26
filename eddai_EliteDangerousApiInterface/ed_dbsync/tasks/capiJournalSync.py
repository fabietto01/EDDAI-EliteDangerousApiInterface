from celery import Task
from celery import group
from celery.utils.log import get_task_logger

from users.models import User
from ed_dbsync.connectors.capi import CapiClient
from ed_dbsync.connectors.capi.exceptions import (
    CapiClinetRequestError, JournalPartialContentError, JournalNoContentError,
    CapiClinetAuthError
)

from ed_dbsync.dataclass import IncomingData
from ed_dbsync.tasks import AnalystTasck

import datetime
from django.utils.timezone import now

from users.utility import refresh_frontier_token

log = get_task_logger(__name__)

class CapiJournalSync(Task):

    name = 'ed_dbsync.tasks.CapiJournalSync'
    ignore_result = True

    max_retries = 3
    retry_backoff = 60  # 1 minuto
    retry_backoff_max = 60 * 10 # 10 minuti
    autoretry_for = (JournalPartialContentError, CapiClinetAuthError)

    @staticmethod
    def get_task_name_for_periodic_task(user: User) -> str:
        return f"CapiJournalSync_for_userid-{user.id}"

    def run(self, user_id: int, *args, **kwargs):
        """
        Synchronizes a user's Elite Dangerous journal entries from the Companion API (CAPI).
        Retrieves journal entries for the specified user, then processes them by creating
        analyst tasks for each entry. Handles authentication issues by attempting to refresh
        Frontier tokens when necessary.
        Args:
            user_id (int): The ID of the user whose journal entries should be synchronized.
            *args: Additional positional arguments passed to the CAPI client's get_journal method.
            **kwargs: Additional keyword arguments:
                - yesterday (bool): If True, retrieves journal entries from the previous day.
                - Other kwargs are passed directly to the CAPI client's get_journal method.
        Raises:
            User.DoesNotExist: If no user with the specified ID exists.
            JournalNoContentError: If no journal entries are found for the specified date.
            CapiClinetRequestError: If there's an error communicating with the CAPI.
            Exception: For any other unexpected errors during synchronization.
        Note:
            This method will retry operations in case of authentication errors (after attempting
            to refresh the token) or when partial content is received from the CAPI.
        """
        try:

            user = User.objects.get(id=user_id)
            log.info(f"Starting CAPI journal sync for user: {user.username} (ID: {user_id})")

            client = CapiClient.from_task(user)

            yesterday = kwargs.get('yesterday', False)
            if yesterday:
                data = now() - datetime.timedelta(days=1)
                kwargs['data'] = data.strftime('%Y/%m/%d')

            token_expired_at = client.get_social_token().expires_at
            if token_expired_at and token_expired_at < now():
                log.warning(f"Token for user {user.username} (ID: {user_id}) is expired. Attempting to refresh token...")
                if not refresh_frontier_token(user=user):
                    raise CapiClinetAuthError()
            
            log.info(f"Creating CAPI client for user: {user.username} (ID: {user_id})")
            journal_entries = client.get_journal(*args, **kwargs)
        
            if not journal_entries:
                log.debug("No journal entries found for the user.")
                return
            
            log.info(f"Found {len(journal_entries)} journal entries to process for user: {user.username} (ID: {user.id})")

            tasks = group(
                AnalystTasck().s(
                    istance=IncomingData(data=entry, source='capi_api'), agent=user
                ) for entry in journal_entries
            )
            tasks.apply_async(
                queue='ed_dbsync',
            )

            log.info(f"Successfully initiated processing of {len(journal_entries)} journal entries for user: {user.username} (ID: {user.id})")

        except User.DoesNotExist as e: 
            log.error(f"User with id {user_id} does not exist.")
            raise e
        except CapiClinetAuthError as e:
            
            from django_celery_beat.models import PeriodicTask

            task = PeriodicTask.objects.get(
                name=CapiJournalSync.get_task_name_for_periodic_task(user)
            )
            task.enabled = False
            task.save()

        except JournalPartialContentError as e:
            log.warning(f"Partial content received for user {user.username} (ID: {user.id}). Retrying...", exc_info=e)
            raise self.retry(exc=e)
        except JournalNoContentError as e:
            log.error(f"No content found for user {user.username} (ID: {user_id}). This may mean the user has not played today.", exc_info=e)
            raise e
        except CapiClinetRequestError as e:
            log.error(f"CapiClinetRequestError occurred for user {user.username} (ID: {user_id})", exc_info=e)
            raise self.retry(exc=e)
        except Exception as e:
            log.error(f"An unexpected error occurred during CAPI journal sync for user {user.username} (ID: {user_id})", exc_info=e)
            raise self.retry(exc=e)
        finally:
            log.info(f"Finished CAPI journal sync for user: {user.username} (ID: {user_id})")
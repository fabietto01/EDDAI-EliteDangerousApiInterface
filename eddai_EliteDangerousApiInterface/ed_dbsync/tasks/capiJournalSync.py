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

from users.utility import refresh_frontier_token

log = get_task_logger(__name__)

class CapiJournalSync(Task):

    name = 'ed_dbsync.tasks.CapiJournalSync'
    ignore_result = True

    max_retries = 3
    retry_backoff = 60  # 1 minuto
    retry_backoff_max = 60 * 10 # 10 minuti
    autoretry_for = (JournalPartialContentError, CapiClinetAuthError)

    def run(self, user_id: int, *args, **kwargs):
        
        try:

            user = User.objects.get(id=user_id)
            log.info(f"Starting CAPI journal sync for user: {user.username} (ID: {user_id})")

            client = CapiClient.from_task(user)

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
            if refresh_frontier_token(user=user):
                log.warning(f"Token refreshed for user {user.username} (ID: {user.id}). Retrying CAPI journal sync...", exc_info=e)
                raise self.retry(exc=e)
            log.warning(f"Failed to refresh token for user {user.username} (ID: {user.id}). CAPI journal sync will not be retried.", exc_info=e)
        except JournalPartialContentError as e:
            log.warning(f"Partial content received for user {user.username} (ID: {user.id}). Retrying...", exc_info=e)
            raise self.retry(exc=e)
        except JournalNoContentError as e:
            log.error(f"No content found for user {user.username} (ID: {user_id}). This may mean the user has not played today.", exc_info=e)
            raise e
        except CapiClinetRequestError as e:
            log.error(f"CapiClinetRequestError occurred for user {user.username} (ID: {user_id})", exc_info=e)
            raise e
        except Exception as e:
            log.error(f"An unexpected error occurred during CAPI journal sync for user {user.username} (ID: {user_id})", exc_info=e)
            raise e
        finally:
            log.info(f"Finished CAPI journal sync for user: {user.username} (ID: {user_id})")
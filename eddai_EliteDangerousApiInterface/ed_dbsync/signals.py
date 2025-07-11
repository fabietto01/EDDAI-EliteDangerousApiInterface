from django.dispatch import receiver
from allauth.socialaccount.signals import social_account_updated, social_account_removed
import logging

from users.models import User
from allauth.socialaccount.models import SocialLogin, SocialAccount

from ed_dbsync.tasks.capiJournalSync import CapiJournalSync

from django_celery_beat.models import PeriodicTask, IntervalSchedule

log = logging.getLogger(__name__)

@receiver(social_account_updated)
def update_social_account(sender, **kwargs):
    log.info("DEBUG: social_account_updated signal received", {"kwargs": kwargs})

@receiver(social_account_removed)
def remove_social_account(sender, **kwargs):
    log.info("DEBUG: social_account_removed signal received", {"kwargs": kwargs})

# @receiver(social_account_updated)
# def update_social_account(sender, request, sociallogin:SocialLogin, **kwargs):
#     """
#     Signal handler for when a social account is updated.
#     This can be used to refresh the user's CAPI token or perform other actions.

#     Args:
#         sender: The sender of the signal.
#         request: The HTTP request object.
#         sociallogin: The social login instance containing the updated account information.
#         **kwargs: Additional keyword arguments.
#     """
#     log.info(f"Social account updated for user: {sociallogin.user.username} (ID: {sociallogin.user.id}). Provider {sociallogin.provider} ", exc_info={"sociallogin": sociallogin})
#     print(f"Social account updated for user: {sociallogin.user.username} (ID: {sociallogin.user.id}). Provider {sociallogin.provider} ")
#     if sociallogin.provider != 'frontier':
#         log.info(f"Social account updated for non-frontier provider: {sociallogin.provider}")
#         return
    
#     user:User = sociallogin.user
#     log.info(f"Social account updated for user: {user.username}")
#     interval_schedule, create = IntervalSchedule.objects.get_or_create(
#         every=24,  # 24 hours
#         period=IntervalSchedule.HOURS,
#     )
#     defaults={
#         'task': CapiJournalSync.name,
#         'interval': interval_schedule,
#         'enabled': True,
#         'one_off': False,
#         'queue': 'ed_dbsync',
#         'args': [],
#         'kwargs': str({'user_id': f'{user.id}'}).replace("'", '"'),
#         'description': f"Sync CAPI journal for user {user.username} (ID: {user.id})",
#     }
#     PeriodicTask.objects.update_or_create(
#         name=CapiJournalSync.get_task_name_for_periodic_task(user),
#         defaults=defaults
#     )
#     log.info(f"Periodic task for CAPI journal sync created/updated for user: {user.username} (ID: {user.id})")

# @receiver(social_account_removed)
# def remove_social_account(sender, request, socialaccount:SocialAccount, **kwargs):
#     """
#     Signal handler for when a social account is removed.
#     This can be used to stop the user's CAPI journal sync task.

#     Args:
#         sender: The sender of the signal.
#         request: The HTTP request object.
#         sociallogin: The social login instance containing the account information.
#         **kwargs: Additional keyword arguments.
#     """
#     if socialaccount.provider != 'frontier':
#         return
    
#     user:User = socialaccount.user
#     log.info(f"Social account removed for user: {user.username}")
#     try:
#         tasck = PeriodicTask.objects.get(name=CapiJournalSync.get_task_name_for_periodic_task(user))
#         tasck.delete()
#         log.info(f"Periodic task for CAPI journal sync removed for user: {user.username} (ID: {user.id})")
#     except PeriodicTask.DoesNotExist:
#         log.warning(f"No periodic task found for user: {user.username} (ID: {user.id})")
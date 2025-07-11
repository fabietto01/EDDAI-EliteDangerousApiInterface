from django.dispatch import receiver
from django.db.models.signals import post_delete
from allauth.socialaccount.signals import social_account_updated, social_account_removed, social_account_added
from allauth.account.signals import user_signed_up
import logging

from users.models import User
from allauth.socialaccount.models import SocialLogin, SocialAccount

from ed_dbsync.tasks.capiJournalSync import CapiJournalSync
from django_celery_beat.models import PeriodicTask, IntervalSchedule

log = logging.getLogger("django.ed_dbsync.signals")

def _remove_sync_task(user:User):
    """
    Helper function to remove the CAPI journal sync task for a user.
    
    Args:
        user: The user whose sync task should be removed.
    """
    try:
        task = PeriodicTask.objects.get(name=CapiJournalSync.get_task_name_for_periodic_task(user))
        task.delete()
        log.info(f"Periodic task for CAPI journal sync removed for user: {user.username} (ID: {user.id})")
    except PeriodicTask.DoesNotExist:
        log.warning(f"No periodic task found for user: {user.username} (ID: {user.id})")

def _setup_capi_sync_task(user:User):
    """
    Helper function to set up the CAPI journal sync task for a user.
    
    Args:
        user: The user for whom to set up the sync task.
    """
    interval_schedule, create = IntervalSchedule.objects.get_or_create(
        every=24,  # 24 hours
        period=IntervalSchedule.HOURS,
    )
    defaults={
        'task': CapiJournalSync.name,
        'interval': interval_schedule,
        'enabled': True,
        'one_off': False,
        'queue': 'ed_dbsync',
        'args': [],
        'kwargs': str({'user_id': f'{user.id}'}).replace("'", '"'),
        'description': f"Sync CAPI journal for user {user.username} (ID: {user.id})",
    }
    PeriodicTask.objects.update_or_create(
        name=CapiJournalSync.get_task_name_for_periodic_task(user),
        defaults=defaults
    )
    log.info(f"Periodic task for CAPI journal sync created/updated for user: {user.username} (ID: {user.id})")

@receiver(social_account_updated)
def update_social_account(sender, request, sociallogin:SocialLogin, **kwargs):
    """
    Signal handler for when a social account is updated.
    This can be used to refresh the user's CAPI token or perform other actions.

    Args:
        sender: The sender of the signal.
        request: The HTTP request object.
        sociallogin: The social login instance containing the updated account information.
        **kwargs: Additional keyword arguments.
    """
    if sociallogin.account.provider != 'frontier':
        log.info(f"Social account updated for non-frontier provider: {sociallogin.account.provider}")
        return
    
    user:User = sociallogin.user
    log.info(f"Frontier account updated for user: {user.username} (ID: {user.id})")
    _setup_capi_sync_task(user)

@receiver(social_account_removed)
def remove_social_account(sender, request, socialaccount:SocialAccount, **kwargs):
    """
    Signal handler for when a social account is removed.
    This can be used to stop the user's CAPI journal sync task.

    Args:
        sender: The sender of the signal.
        request: The HTTP request object.
        socialaccount: The social account instance being removed.
        **kwargs: Additional keyword arguments.
    """
    user:User = socialaccount.user
    log.info(f"Social account removed for user: {user.username}")

    if socialaccount.provider != 'frontier':
        return
    
    _remove_sync_task(user)

@receiver(post_delete, sender=User)
def user_deleted(sender, instance:User, **kwargs):
    """
    Signal handler for when a user is deleted.
    This removes any CAPI journal sync tasks for the user.

    Args:
        sender: The sender of the signal.
        instance: The user instance being deleted.
        **kwargs: Additional keyword arguments.
    """
    log.info(f"User deleted: {instance.username} (ID: {instance.id})")
    _remove_sync_task(instance)

@receiver(user_signed_up)
def update_account_on_signup(sender, user:User, **kwargs):
    """
    Signal handler for when a user signs up.
    If the user signed up with Frontier, set up the CAPI journal sync task.

    Args:
        sender: The sender of the signal.
        user: The user who signed up.
        **kwargs: Additional keyword arguments.
    """
    try:
        log.info(f"Signal: user_signed_up ricevuto per user {user.id}")
        
        if not SocialAccount.objects.filter(user=user, provider='Frontier').exists():
            log.info(f"No Frontier account found for user {user.username} (ID: {user.id}), skipping CAPI sync setup")
            return
        
        log.info(f"User {user.username} (ID: {user.id}) signed up with Frontier, setting up CAPI sync")
        _setup_capi_sync_task(user)
    except Exception as e:
        log.error(f"Error setting up CAPI sync for new user {user.id}", exc_info=e)

@receiver(social_account_added)
def update_account_on_connect(sender, request, sociallogin:SocialLogin, **kwargs):
    """
    Signal handler for when a social account is added.
    If the user connected a Frontier account, set up the CAPI journal sync task.

    Args:
        sender: The sender of the signal.
        request: The HTTP request object.
        sociallogin: The social login instance.
        **kwargs: Additional keyword arguments.
    """
    if sociallogin.account.provider != 'Frontier':
        log.info(f"Social account added for non-Frontier provider: {sociallogin.account.provider}")
        return
        
    user:User = sociallogin.user
    log.info(f"Signal: social_account_added ricevuto per user {user.id}")
    log.info(f"User {user.username} (ID: {user.id}) connected Frontier account, setting up CAPI sync")
    _setup_capi_sync_task(user)
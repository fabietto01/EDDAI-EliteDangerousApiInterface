from django.dispatch import receiver
from allauth.socialaccount.signals import social_account_added
from .utility import get_cmdr_name

from .models import User
import logging

log = logging.getLogger(__name__)

@receiver(social_account_added)
def update_cmdr_profile(sender, request, sociallogin, **kwargs):
    """
    Aggiorna il profilo CMDR quando un account social viene aggiornato
    """
    try:
        if sociallogin.account.provider == 'frontier':
            user:User = sociallogin.user

            username = get_cmdr_name(user)

            if username and username != user.username:
                user.username = username
                user.save()
    except Exception as e:
        log.error(f"Error updating CMDR profile for user {user.id}: {e}", exc_info=True)
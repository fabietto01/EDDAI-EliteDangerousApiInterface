from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from allauth.socialaccount.models import SocialAccount
from .utility import get_cmdr_name

from .models import User
import logging

log = logging.getLogger("django")

@receiver(user_signed_up)
def update_cmdr_profile(sender, user:User, **kwargs):
    """
    Aggiorna il profilo CMDR quando un account social viene aggiornato
    """
    try:
        if not SocialAccount.objects.filter(user=user, provider='Frontier').exists():
            log.info(f"No Frontier social account found for user {user.id}, skipping CMDR profile update.")
            return
        
        username = get_cmdr_name(user)

        if username and username != user.username:
            user.username = username
            user.save()
    except Exception as e:
        log.error(f"Error updating CMDR profile for user {user.id}", exc_info=e)
from django.dispatch import receiver
from allauth.socialaccount.signals import social_account_added
from allauth.socialaccount.models import SocialLogin
from .utility import get_cmdr_name

from .models import User
import logging

log = logging.getLogger("django")

@receiver(social_account_added)
def update_cmdr_profile(sender, request, sociallogin:SocialLogin, **kwargs):
    """
    Aggiorna il profilo CMDR quando un account social viene aggiornato
    """
    log.info(f"Social account updated for user: {sociallogin.user.username} (ID: {sociallogin.user.id}). Provider {sociallogin.provider} ", exc_info={"sociallogin": sociallogin})
    print(f"Social account updated for user: {sociallogin.user.username} (ID: {sociallogin.user.id}). Provider {sociallogin.provider} ")
    try:
        if sociallogin.provider != 'frontier':
            log.info(f"Social account updated for non-frontier provider: {sociallogin.provider}")
            return
        
        user:User = sociallogin.user

        username = get_cmdr_name(user)

        if username and username != user.username:
            user.username = username
            user.save()
    except Exception as e:
        log.error(f"Error updating CMDR profile for user {user.id}", exc_info=e)
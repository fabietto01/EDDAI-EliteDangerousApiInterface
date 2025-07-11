from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import social_account_added
from allauth.socialaccount.models import SocialAccount, SocialLogin
from .utility import get_cmdr_name

from .models import User
import logging

log = logging.getLogger("django")

@receiver(user_signed_up)
def update_cmdr_profile(sender, user:User, **kwargs):
    """
    Aggiorna il profilo CMDR quando un utente si registra
    """
    try:

        log.info(f"User signed up: {user.id}, updating CMDR profile.")

        if not SocialAccount.objects.filter(user=user, provider='frontier').exists():
            log.info(f"No Frontier social account found for user {user.id}, skipping CMDR profile update.")
            return
        
        username = get_cmdr_name(user)

        if username and username != user.username:
            user.username = username
            user.save()
            log.debug(f"CMDR profile updated for user {user.id} with username {username}")
        else:
            log.debug(f"No change in CMDR profile for user {user.id}, username remains {user.username}")

        log.info(f"CMDR profile updated for user {user.id} with username {username}")

    except Exception as e:
        log.error(f"Error updating CMDR profile for user {user.id}", exc_info=e)

@receiver(social_account_added)
def update_cmdr_profile_on_connect(sender, request, sociallogin:SocialLogin, **kwargs):
    """
    Aggiorna il profilo CMDR quando un account Frontier viene collegato
    """
    try:

        user = sociallogin.user
        log.info(f"Frontier account connected for user {user.id}, updating CMDR profile.")

        if not sociallogin or sociallogin.account.provider != 'frontier':
            log.info("Social login is not for Frontier provider, skipping CMDR profile update.")
            return
            
        username = get_cmdr_name(user)
        
        if username and username != user.username:
            user.username = username
            user.save()
            log.debug(f"CMDR profile updated for user {user.id} with username {username}")
        else:
            log.debug(f"No change in CMDR profile for user {user.id}, username remains {user.username}")

        log.info(f"CMDR profile updated for user {user.id} with username {username}")

    except Exception as e:
        if sociallogin and sociallogin.user:
            user_id = sociallogin.user.id
        else:
            user_id = "unknown"
        log.error(f"Error updating CMDR profile on connect for user {user_id}", exc_info=e)
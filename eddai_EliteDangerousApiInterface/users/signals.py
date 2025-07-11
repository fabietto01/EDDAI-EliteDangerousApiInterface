from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from allauth.socialaccount.signals import social_account_added
from allauth.socialaccount.models import SocialAccount, SocialLogin
from .utility import get_cmdr_name

from .models import User
import logging

log = logging.getLogger("django.user.signals")

def _update_cmdr_username(user, description=""):
    """
    Funzione comune per aggiornare il nome utente CMDR
    
    Args:
        user (User): Utente da aggiornare
        description (str): Descrizione dell'operazione per i log
    
    Returns:
        bool: True se l'aggiornamento è avvenuto, False altrimenti
    """
    try:
        username = get_cmdr_name(user)
        
        if username and username != user.username:
            user.username = username
            user.save()
            return True
        
        return False
    except Exception as e:
        user_id = getattr(user, 'id', 'unknown')
        log.error(f"Error updating CMDR profile {description} for user {user_id}", exc_info=e)
        return False

@receiver(user_signed_up)
def update_cmdr_profile(sender, user:User, **kwargs):
    """
    Aggiorna il profilo CMDR quando un utente si registra
    """
    try:
        log.info(f"Signal: user_signed_up ricevuto per user {user.id}")
        
        if not SocialAccount.objects.filter(user=user, provider='frontier').exists():
            return
        
        _update_cmdr_username(user, "at signup")
        
    except Exception as e:
        log.error(f"Error in user_signed_up signal for user {user.id}", exc_info=e)

@receiver(social_account_added)
def update_cmdr_profile_on_connect(sender, request, sociallogin:SocialLogin, **kwargs):
    """
    Aggiorna il profilo CMDR quando un account Frontier viene collegato
    """
    try:
        user = sociallogin.user
        log.info(f"Signal: social_account_added ricevuto per user {user.id}")
        
        if not sociallogin or sociallogin.account.provider != 'frontier':
            return
            
        _update_cmdr_username(user, "on connect")
        
    except Exception as e:
        user_id = getattr(getattr(sociallogin, 'user', None), 'id', 'unknown')
        log.error(f"Error in social_account_added signal for user {user_id}", exc_info=e)
from django.dispatch import receiver
from allauth.socialaccount.signals import social_account_updated, social_account_added
from .utility import get_cmdr_name

from .models import User

@receiver(social_account_added)
def update_cmdr_profile(sender, request, sociallogin, **kwargs):
    """
    Aggiorna il profilo CMDR quando un account social viene aggiornato
    """
    if sociallogin.account.provider == 'frontier':
        user:User = sociallogin.user

        username = get_cmdr_name(user)

        if username:
            user.username = username
            user.save()

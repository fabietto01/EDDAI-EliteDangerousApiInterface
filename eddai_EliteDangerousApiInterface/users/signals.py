from allauth.socialaccount.signals import social_account_updated
from django.dispatch import receiver


@receiver(social_account_updated)
def social_account_updated_handler(request, sociallogin, **kwargs):
    """
    Signal handler for when a social account is updated.
    """
    
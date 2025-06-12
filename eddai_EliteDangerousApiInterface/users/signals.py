from allauth.account.signals import user_logged_in, user_signed_up
from allauth.socialaccount.signals import pre_social_login, social_account_added, social_account_updated
from django.dispatch import receiver

import logging
logger = logging.getLogger(__name__)

@receiver(user_logged_in)
def user_logged_in_handler(request, user, **kwargs):
    """
    Signal handler for user login.
    """
    logger.info(f"User {user.username} logged in.", extra={
        'user': user,
        'request': request,
    })
    # You can add additional logic here if needed

@receiver(user_signed_up)
def user_signed_up_handler(request, user, **kwargs):
    """
    Signal handler for user signup.
    """
    logger.info(f"User {user.username} signed up.", extra={
        'user': user,
        'request': request,
    })
    # You can add additional logic here if needed


@receiver(pre_social_login)
def pre_social_login_handler(request, sociallogin, **kwargs):
    """
    Signal handler for pre-social login.
    """
    logger.info(f"Pre-social login for user {sociallogin.user.username} with provider {sociallogin.account.provider}.", extra={
        'sociallogin': sociallogin,
        'request': request,
    })
    # You can add additional logic here if needed

@receiver(social_account_added)
def social_account_added_handler(request, sociallogin, **kwargs):
    """
    Signal handler for when a social account is added.
    """
    logger.info(f"Social account added for user {sociallogin.user.username} with provider {sociallogin.account.provider}.", extra={
        'sociallogin': sociallogin,
        'request': request,
    })
    # You can add additional logic here if needed

@receiver(social_account_updated)
def social_account_updated_handler(request, sociallogin, **kwargs):
    """
    Signal handler for when a social account is updated.
    """
    logger.info(f"Social account updated for user {sociallogin.user.username} with provider {sociallogin.account.provider}.", extra={
        'sociallogin': sociallogin,
        'request': request,
    })
    # You can add additional logic here if needed
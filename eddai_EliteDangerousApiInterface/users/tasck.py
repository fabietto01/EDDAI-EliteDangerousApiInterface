from celery import shared_task

from allauth.socialaccount.models import SocialToken

@shared_task
def get_social_token():
    pass
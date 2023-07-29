from celery import Celery
from django_service.settings import servis_settings
from django.utils.module_loading import import_string


def get_celery_app()->Celery:
    return import_string(servis_settings.SERVICES_CELERY_APP)
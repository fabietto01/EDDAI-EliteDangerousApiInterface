from celery import Celery
from django_service.settings import servis_settings

class ServiceCelery(Celery):

    def autodiscover_tasks(self, packages=None,
                           related_name='tasks', force=False):
        super().autodiscover_tasks(packages, related_name, force)
        related_name = servis_settings.SERVICE_RELARED_NAME
        super().autodiscover_tasks(packages, related_name, force)
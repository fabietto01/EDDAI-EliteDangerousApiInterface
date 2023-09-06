from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class DjangoServiceConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'django_service'
    verbose_name  = _('Djnago manege service')

    def ready(self):
        from .checks import celery_check
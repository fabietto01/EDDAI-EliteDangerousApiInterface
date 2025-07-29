from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EdDbsyncConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ed_dbsync'
    verbose_name = _('ed Database Sync')

    def ready(self):
        import ed_dbsync.signals

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EdDbsyncConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ed_dbsync'
    verbose_name = _('ed Database Sync')

    def ready(self):
        """
        This method is called when the application is ready.
        It can be used to perform any initialization tasks or register signals.
        """
        # Import signals or other modules that need to be initialized
        from ed_dbsync import signals

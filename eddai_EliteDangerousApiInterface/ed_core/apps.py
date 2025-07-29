from django.apps import AppConfig


class EdCoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ed_core'

    def ready(self):
        import ed_core.extensions
from django.apps import AppConfig


class EddnConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'eddn'


    def ready(self) -> None:
        import eddn.signals
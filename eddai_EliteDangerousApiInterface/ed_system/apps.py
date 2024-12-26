from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class EdSystemConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ed_system'
    verbose_name = _("system")

from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _

class EdBgsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ed_bgs'
    verbose_name = _("bgs")

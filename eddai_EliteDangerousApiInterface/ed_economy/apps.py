from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EdEconomyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ed_economy'
    verbose_name = _("economy")

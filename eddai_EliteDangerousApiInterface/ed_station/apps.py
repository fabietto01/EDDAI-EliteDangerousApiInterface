from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EdStationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ed_station'
    verbose_name = _("Station")
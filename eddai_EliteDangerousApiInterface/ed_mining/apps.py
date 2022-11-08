from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EdMiningConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ed_mining'
    verbose_name = _("mining")


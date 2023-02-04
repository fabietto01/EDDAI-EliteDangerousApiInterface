from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EdExplorationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ed_exploration'
    verbose_name = _("exploration")

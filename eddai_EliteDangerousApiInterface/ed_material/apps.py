from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class EdMaterialConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ed_material'
    verbose_name = _("material")

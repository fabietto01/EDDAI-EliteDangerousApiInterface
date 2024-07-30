from django.db import models
from django.utils.translation import gettext_lazy as _

from eddn.models import AbstractDataEDDN
from core.models import CacheModel

class HotspotType(AbstractDataEDDN, CacheModel, models.Model):
    name = models.CharField(
        max_length=255, unique=True, verbose_name=_('name')
    )
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Hotspot Type")
        verbose_name_plural = _("Hotspot Type")

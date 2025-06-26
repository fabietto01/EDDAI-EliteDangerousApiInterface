from django.db import models
from django.utils.translation import gettext_lazy as _

from ed_dbsync.models import AbstractDataEDDN

class HotspotType(AbstractDataEDDN, models.Model):
    name = models.CharField(
        max_length=255, unique=True, verbose_name=_('name')
    )
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Hotspot Type")
        verbose_name_plural = _("Hotspot Type")
        ordering = ['name']

from django.db import models
from django.utils.translation import gettext_lazy as _

from ed_dbsync.models import AbstractDataEDDN

class SampleSignals(AbstractDataEDDN, models.Model):
    """
    contiene tutti i tipo di Campioni possibili per un pianeta
    """
    name = models.CharField(
        max_length=255, unique=True, verbose_name=_('name')
    )
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("Sample type")
        verbose_name_plural = _("Samples type")
        ordering = ['name']
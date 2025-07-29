from django.db import models
from django.utils.translation import gettext_lazy as _

from ed_dbsync.models import AbstractDataEDDN

class Government(AbstractDataEDDN, models.Model):
    """
    modello per la memorizazione dei governi presenti in ED
    """
    class TipeChoices(models.TextChoices):
        """
        valori possibili per il tipo di governo
        """
        Anarchy = 'A', _('Anarchy')
        Autocrati = 'C', _('Autocrati')
        Corporazioni = 'P', _('Corporazioni')
        Social = 'S', _('Social')

    name = models.CharField(
        max_length=255, unique=True, verbose_name=_('name')
    )
    type=models.CharField(
        max_length=1,
        choices=TipeChoices.choices,
        verbose_name=_('type'),
        null=True, blank=True
    )
    description = models.TextField(
        blank=True, null=True,
        verbose_name=_('description')
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _('government')
        verbose_name_plural = _('governments')
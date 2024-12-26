from django.db import models
from django.utils.translation import gettext_lazy as _

from eddn.models import AbstractDataEDDN

class Commodity(AbstractDataEDDN, models.Model):
    """
    modello dedicatto alla gestione dei dati di una commodity
    """

    name = models.CharField(
        max_length=100, unique=True, verbose_name=_('name')
    )
    description = models.TextField(
        blank=True, null=True
    )
    meanPrice = models.IntegerField(
        verbose_name=_('mean price')
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _('commodity')
        verbose_name_plural = _('commodities')
        ordering = ['name']
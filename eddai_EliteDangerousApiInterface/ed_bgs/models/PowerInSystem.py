from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import OwnerAndDateModels
from ed_bgs.models import Power, PowerState

class PowerInSystem(OwnerAndDateModels):
    """
    modelo corellato 1:1 con il modelo system contente le informazioni
    riguradanti le Power all interno del systema, avra una relazione n:n con
    il modello Power
    """
    system = models.ForeignKey(
        'ed_system.System', on_delete=models.CASCADE,
        verbose_name=_('system'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )
    power = models.ForeignKey(
        Power, on_delete=models.CASCADE,
        verbose_name=_('Power'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )
    state = models.ForeignKey(
        PowerState, on_delete=models.PROTECT,
        verbose_name=_('state'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss',
    )

    @property
    def MaxRelation(self):
        return 2
    
    @property
    def StateForMoreRellation(self):
        return ('Contested')

    def __str__(self) -> str: 
        return f"{self.state} for {self.power} in {self.system}"

    class Meta:
        verbose_name = _('Power in System')
        verbose_name_plural = _('Powers in Systems')
        ordering = ('system',)
        indexes = [
            models.Index(fields=['state']),
            models.Index(fields=['system']),
            models.Index(fields=['power']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['system', 'power'], name='unique_power_in_system'),
        ]

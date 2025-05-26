from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import OwnerAndDateModels
from ed_bgs.models import Power, PowerState

from core.utility import  get_or_none

class PowerInSystem(OwnerAndDateModels):
    """
    Represents the relationship between a power, a system, and its state.
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

    @staticmethod
    def get_max_relations():
        """
        Returns the maximum relation value.
        """
        return 12

    @staticmethod
    def StateForMoreRellation() -> PowerState:
        """
        Returns the PowerState object for more relation.
        """
        return get_or_none(PowerState, name='Contested')

    def __str__(self) -> str: 
        """
        Returns a string representation of the PowerInSystem object.
        """
        return f"{self.power} in {self.system}"

    class Meta:
        verbose_name = _('Power in System')
        verbose_name_plural = _('Powers in Systems')
        ordering = ('system',)
        indexes = [
            models.Index(fields=['state']),
            models.Index(fields=['power'])
        ]
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import OwnerAndDateModels

from ed_bgs.models.Faction import Faction
from ed_bgs.models.Government import Government


class MinorFaction(OwnerAndDateModels):
    """
    modello utilizato per memorizare le minori fazioni presenti in ED
    """
    name = models.CharField(
        max_length=255, unique=True, verbose_name=_('name')
    )
    allegiance = models.ForeignKey(
        Faction, on_delete=models.PROTECT,
        default=Faction.get_default,
        verbose_name=_('allegiance'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss',
    )
    government = models.ForeignKey(
        Government, on_delete=models.PROTECT,
        verbose_name=_('government'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss',
        null=True
    )
    description = models.TextField(
        blank=True, null=True,
        verbose_name=_('description')
    )

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = _('Minor Faction')
        verbose_name_plural = _('Minor Factions')
        indexes = [
            models.Index(fields=['allegiance'], name='idx_minor_faction_allegiance'),
            models.Index(fields=['government'], name='idx_minor_faction_government'),
        ]
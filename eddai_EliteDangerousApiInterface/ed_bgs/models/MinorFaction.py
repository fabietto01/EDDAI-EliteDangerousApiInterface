from django.db import models
from django.utils.translation import gettext_lazy as _

from ed_bgs.models.Faction import Faction, default_faction
from ed_bgs.models.Government import Government


class MinorFaction(models.Model):
    """
    modello utilizato per memorizare le minori fazioni presenti in ED
    """
    name = models.CharField(
        max_length=255, unique=True, verbose_name=_('name')
    )
    allegiance = models.ForeignKey(
        Faction, on_delete=models.PROTECT,
        default=default_faction,
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
    updated = models.DateTimeField(
        auto_now=True
    )

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = _('Minor Faction')
        verbose_name_plural = _('Minor Factions')
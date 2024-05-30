from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import OwnerAndDateModels

from ed_bgs.models import MinorFaction

class MinorFactionInSystem(OwnerAndDateModels):
    system = models.ForeignKey(
        'ed_system.System', on_delete=models.CASCADE,
        verbose_name=_('system'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )
    minorFaction = models.ForeignKey(
        MinorFaction, on_delete=models.CASCADE,
        verbose_name=_('Minor Faction'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )
    Influence = models.FloatField(
        verbose_name=_('Influence'),
        null=True, blank=True
    )

    @property
    def MaxRelation(self):
        return 8

    def __str__(self) -> str:
        return str(self.minorFaction)

    class Meta:
        verbose_name = _('Minor Faction in System')
        verbose_name_plural = _('Minor Factions in Systems')
        ordering = ('system', 'minorFaction')
        indexes = [
            models.Index(fields=['system'], name='system_idx'),
            models.Index(fields=['minorFaction'], name='minorFaction_idx'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['minorFaction','system'], name='unique_minosrs_faction_in_system'),
        ]

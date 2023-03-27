from django.db import models
from django.utils.translation import gettext_lazy as _

class MinorFactionInSystem(models.Model):

    MaxRelation = 8

    system = models.ForeignKey(
        'ed_system.System', on_delete=models.CASCADE,
        verbose_name=_('system'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )
    minorFaction = models.ForeignKey(
        'ed_bgs.MinorFaction', on_delete=models.CASCADE,
        verbose_name=_('Minor Faction'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )
    Influence = models.FloatField(
        verbose_name=_('Influence'),
        null=True, blank=True
    )
    updated = models.DateTimeField(
        auto_now=True
    )

    @property
    def happiness(self):
        pass

    def __str__(self) -> str:
        return str(self.system) + " - " + str(self.minorFaction)

    class Meta:
        verbose_name = _('Minor Faction in System')
        verbose_name_plural = _('Minor Factions in Systems')
        ordering = ('system', 'minorFaction')
        indexes = [
            models.Index(fields=['system', 'minorFaction']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['minorFaction','system'], name='unique_minosrs_faction_in_system'),
        ]

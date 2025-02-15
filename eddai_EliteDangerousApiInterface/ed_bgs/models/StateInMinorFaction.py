from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import OwnerAndDateModels

from .MinorFactionInSystem import MinorFactionInSystem
from .State import State

class StateInMinorFaction(OwnerAndDateModels):
    """
    modello utilizato per memorizzare la relazione tra stato e Minor Faction
    presente al interno di un sistema per esaltezza questo ultimo e la relazione tra minor faction 
    e Systema
    """
    class PhaseChoices(models.TextChoices):
        """
        tipi di fassi che possiede uno statto
        """
        RECOVERING = 'R', _('Recovering')
        ACTIVE = 'A', _('Active')
        PENDING = 'P', _('Pending')
        
    minorFaction = models.ForeignKey(
        MinorFactionInSystem, on_delete=models.CASCADE,
        verbose_name=_('Minor Faction'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )
    state = models.ForeignKey(
        State, on_delete=models.PROTECT,
        verbose_name=_('state'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )
    phase = models.CharField(
        max_length=1, choices=PhaseChoices.choices,
    )

    def __str__(self) -> str:
        return f"{self.state}"

    class Meta:
        verbose_name = _('State from the Minor Faction')
        verbose_name_plural = _('States from the Minor Factions')
        ordering = ('minorFaction', 'state')
        indexes = [
            models.Index(fields=['minorFaction']),
            models.Index(fields=['state']),
            models.Index(fields=['phase']),
        ]
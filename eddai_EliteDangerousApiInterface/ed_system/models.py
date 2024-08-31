from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.db.models import Value
from django.db.models.functions import Concat

from core.models import OwnerAndDateModels

from ed_economy.models import Economy
from ed_bgs.models.MinorFaction import MinorFaction
from ed_bgs.models.MinorFactionInSystem import MinorFactionInSystem

class System(OwnerAndDateModels, models.Model):
    """
    modello deditatto al salvatagio dei dati generici riguardanti i sistemmi dati mode:
    nome, coordinata x, coordinata y, coordinata z, descrizione, data aggiornamento
    """
    class SecurityChoices(models.TextChoices):
        """
        valori possibili per la scema di sicurezza del sistema
        """
        Low = 'L', _('Low')
        Medium = 'M', _('Medium')
        High = 'H', _('High')
        Anarchy = 'A', _('Anarchy')

    name = models.CharField(
        max_length=100, unique=True, verbose_name=_('name')
    )
    coordinate = models.PointField(
        dim=3, srid=4979,
        verbose_name=_('coordinate'),
        unique=True,
    )
    security = models.CharField(
        verbose_name=_('security'), max_length=1, 
        choices=SecurityChoices.choices, blank=True, null=True
    )
    population = models.PositiveBigIntegerField(
        verbose_name=_('population'), default=0
    )
    primaryEconomy = models.ForeignKey(
        Economy, on_delete=models.SET_NULL, 
        verbose_name=_('Primary economy'), blank=True, null=True,
        related_name='%(app_label)s_%(class)s_primary_related',
        related_query_name='%(app_label)s_%(class)ss_primary'
    )
    secondaryEconomy = models.ForeignKey(
        Economy, on_delete=models.SET_NULL, 
        verbose_name=_('Secondary economy'), blank=True, null=True,
        related_name='%(app_label)s_%(class)s_secondary_related',
        related_query_name='%(app_label)s_%(class)ss_secondary'
    )
    conrollingFaction = models.ForeignKey(
        MinorFaction, on_delete=models.SET_NULL,
        verbose_name=_('controlling faction'), blank=True, null=True,
        related_name='%(app_label)s_%(class)s_controlling_related',
        related_query_name='%(app_label)s_%(class)ss_controlling'
    )
    description = models.TextField(
        blank=True, null=True
    )

    @property
    @admin.display(ordering=Concat("primaryEconomy", Value(" "), "secondaryEconomy"), description=_('economy'))
    def economy(self) -> list[Economy]:
        """
        ritorna l'economia della systema
        """
        if self.primaryEconomy == None and self.secondaryEconomy == None:
            return None
        elif self.secondaryEconomy == None:
            return [self.primaryEconomy]
        return [self.primaryEconomy, self.secondaryEconomy]

    def clean(self) -> None:
        if self.conrollingFaction != None:
            if not MinorFactionInSystem.objects.filter(system=self, minorFaction=self.conrollingFaction).exists():
                raise ValidationError(_('the controlling faction is not present in the system'))

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('System')
        verbose_name_plural = _('Systems')
        constraints = [
            
        ]
        indexes = [
            models.Index(fields=['primaryEconomy', 'secondaryEconomy'], name='system_economy_idx'),
            models.Index(fields=['conrollingFaction'], name='system_controllingFaction_idx'),
            models.Index(fields=['security'], name='system_security_idx'),
        ]
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.db.models import Value
from django.db.models.functions import Concat

from django.core.validators import MinValueValidator

from core.models import OwnerAndDateModels

from ed_economy.models import Economy
from ed_bgs.models import MinorFaction, MinorFactionInSystem
from .StationType import StationType
from .Service import Service
from .ServiceInStation import ServiceInStation
from ed_economy.models import Commodity
from ed_economy.models import CommodityInStation

class Station(OwnerAndDateModels):
    """
    modello utilizato per memorizzare tutte le stazioni presenti nel gioco
    """
    class LandingPadChoices(models.TextChoices):
        """
        descrive i 3 tipi di pad di atterraggio presneti nel stazioni
        piccolo, medio e grande
        """
        Small = 'S', _('Small')
        Medium = 'M', _('Medium')
        Large = 'L', _('Large')
        __empty__ = _('None')

    name = models.CharField(
        max_length=255, unique=True, verbose_name=_('name')
    )
    system = models.ForeignKey(
        'ed_system.System', on_delete=models.CASCADE,
        verbose_name=_('system'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )
    landingPad = models.CharField(
        max_length=1, choices=LandingPadChoices.choices,
        null=True, 
        verbose_name=_('landing pad')
    )
    type = models.ForeignKey(
        StationType, on_delete=models.PROTECT,
        null=True,
        verbose_name=_('type'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )
    primaryEconomy = models.ForeignKey(
        Economy, on_delete=models.CASCADE,
        null=True,
        verbose_name=_('primary economy'),
        related_name='primary_%(app_label)s_%(class)s_related',
        related_query_name='primary_%(app_label)s_%(class)ss'
    )
    secondaryEconomy = models.ForeignKey(
        Economy, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name=_('secondary economy'),
        related_name='secondary_%(app_label)s_%(class)s_related',
        related_query_name='secondary_%(app_label)s_%(class)ss'
    )
    minorFaction = models.ForeignKey(
        MinorFaction, on_delete=models.CASCADE,
        null=True, blank=True,
        verbose_name=_('Minor Faction'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )
    service = models.ManyToManyField(
        Service, through=ServiceInStation,
        through_fields=('station', 'service'),
        verbose_name=_('service')
    )
    commodity = models.ManyToManyField(
        Commodity, through=CommodityInStation,
        through_fields=('station', 'commodity'),
        verbose_name=_('commodity')
    )
    distance = models.FloatField(
        verbose_name=_('distance'),
        help_text=_('distance from the stary center'),
        validators=[
            MinValueValidator(0, _('the distance cannot be less than 0'))
        ],
        null=True
    )

    def __str__(self) -> str:
        return self.name
    
    def clean(self) -> None:
        if self.primaryEconomy == self.secondaryEconomy :
            raise ValidationError(_('the primary and secondary economy cannot be the same'))
        if self.minorFaction:
            if not MinorFactionInSystem.objects.filter(system=self.system, minorFaction=self.minorFaction).exists():
                raise ValidationError(_('the minor faction is not present in the system'))
        super().clean()
    
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

    class Meta:
        verbose_name = _('station')
        verbose_name_plural = _('stations')
        indexes = [
            models.Index(fields=['system']),
            models.Index(fields=['type']),
            models.Index(fields=['landingPad']),
            models.Index(fields=['primaryEconomy']),
            models.Index(fields=['secondaryEconomy']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['name','system'], name='unique_station_in_system')
        ]

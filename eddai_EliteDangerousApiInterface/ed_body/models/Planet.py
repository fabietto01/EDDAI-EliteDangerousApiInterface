from django.db import models
from django.core.validators import  MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.contrib import admin

from ed_body.models.BaseBody import BaseBody
from ed_body.models.AtmosphereType import AtmosphereType
from ed_body.models.PlanetType import PlanetType
from ed_body.models.Volcanism import Volcanism

class Planet(BaseBody):
    """
    modello per i pianeti
    """
    class TerraformingState(models.TextChoices):
        TERRAFORMABLE = 'Terraformable', _('Terraformable')
        TERRAFORMMING = 'Terraforming', _('Terraforming')
        TERRAFORMMED = 'Terraformed', _('Terraformed')
        NOT_TERRAFORMABLE = '', _('Not Terraformable')
        
    class ReserveLevel(models.TextChoices):
        PRISTINE = 'Pristine', _('Pristine')
        MAJOR = 'Major', _('Major')
        COMMMMON = 'Common', _('Common')
        LOW = 'Low', _('Low')
        DEPLETED = 'Depleted', _('Depleted')

    atmosphereType = models.ForeignKey(
        AtmosphereType, models.PROTECT,
        verbose_name=_('atmosphere type'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss',
        null=True, blank=True,
    )
    planetType = models.ForeignKey(
        PlanetType, models.PROTECT,
        verbose_name=_('planet type'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss',
        null=True, blank=True,
    )
    volcanism = models.ForeignKey(
        Volcanism, models.PROTECT,
        verbose_name=_('volcanism'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss',
        null=True, blank=True,
    )
    terraformState = models.CharField(
        max_length=15,
        choices=TerraformingState.choices,
        verbose_name=_('terraform state'), 
        null=True, blank=True
    )
    _compositionIce = models.FloatField(
        verbose_name=_('ice'),
        validators=[
            MinValueValidator(0, _('the composition ice cannot be less than 0')),
        ],
        null=True, blank=True, 
    )
    _compositionRock = models.FloatField(
        verbose_name=_('rock'),
        validators=[
            MinValueValidator(0, _('the composition rock cannot be less than 0')),
        ],
        null=True, blank=True,
    )
    _compositionMetal = models.FloatField(
        verbose_name=_('metal'),
        validators=[
            MinValueValidator(0, _('the composition metal cannot be less than 0')),
        ],
        null=True, blank=True,
    )
    landable = models.BooleanField(
        verbose_name=_('landable'),
        null=True, blank=True,
    )
    massEM = models.FloatField(
        verbose_name=_('Earth masses'),
        validators=[
            MinValueValidator(0, _('the mass cannot be less than 0')),
        ],
        null=True, blank=True,
    )
    surfaceGravity = models.FloatField(
        verbose_name=_('surface gravity'),
        validators=[
            MinValueValidator(0, _('the surface gravity cannot be less than 0')),
        ],
        null=True, blank=True,
    )
    surfacePressure = models.FloatField(
        verbose_name=_('surface pressure'),
        validators=[
            MinValueValidator(0, _('the surface pressure cannot be less than 0')),
        ],
        null=True, blank=True,
    )
    tidalLock = models.BooleanField(
        verbose_name=_('tidal lock'),
        help_text=_('Tidal locking results in the moon rotating about its axis in about the same time it takes to orbit Body.'),
        null=True, blank=True,
    )
    reserveLevel = models.CharField(
        max_length=10,
        choices=ReserveLevel.choices,
        verbose_name=_('reserve level'),
        null=True, blank=True,
    )

    @property
    @admin.display(description=_('composition'))
    def composition(self) -> dict:
        return {
            'ice': self._compositionIce,
            'rock': self._compositionRock,
            'metal': self._compositionMetal,
        }
    
    class Meta:
        verbose_name = _('planet')
        verbose_name_plural = _('planets')
        indexes = [
            models.Index(fields=['atmosphereType']),
            models.Index(fields=['planetType']),
            models.Index(fields=['volcanism']),
            models.Index(fields=['terraformState']),
            models.Index(fields=['landable']),
            models.Index(fields=['tidalLock']),
            models.Index(fields=['reserveLevel']),
        ]
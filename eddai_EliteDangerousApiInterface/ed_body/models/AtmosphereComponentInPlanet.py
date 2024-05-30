from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

from core.models import OwnerAndDateModels

from ed_body.models.Planet import Planet
from ed_body.models.AtmosphereComponent import AtmosphereComponent

class AtmosphereComponentInPlanet(OwnerAndDateModels):
    """
    modello per i componenti delle atmosfere
    """
    planet = models.ForeignKey(
        Planet, models.CASCADE,
        verbose_name=_('planet'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )
    atmosphere_component = models.ForeignKey(
        AtmosphereComponent, models.PROTECT,
        verbose_name=_('atmosphere component'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )
    percent = models.FloatField(
        verbose_name=_('percent'),
        validators=[
            MinValueValidator(0, _('the percent cannot be less than 0')),
            MaxValueValidator(100, _('the percent cannot be greater than 100')),
        ]
    )

    def __str__(self) -> str:
        return f'{self.atmosphere_component.name}'

    class Meta:
        verbose_name = _('atmosphere component in planet')
        verbose_name_plural = _('atmosphere components in planets')
        indexes = [
            models.Index(fields=['planet'], name='planet_component_planet_idx'),
            models.Index(fields=['atmosphere_component'], name='atmo_component_planet_idx'),
        ]
        constraints = [
            models.UniqueConstraint(fields=['planet', 'atmosphere_component'], name='planet_atmo_component_uc'),
        ]
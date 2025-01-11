from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

from core.models import OwnerAndDateModels

from ed_body.models.Planet import Planet
from ed_body.models.AtmosphereComponent import AtmosphereComponent

class AtmosphereComponentInPlanet(OwnerAndDateModels):
    """
    Represents the relationship between a planet and its atmosphere components, 
    including the percentage of each component in the planet's atmosphere.
    Attributes:
        planet (ForeignKey): A reference to the Planet model, indicating which planet this atmosphere component belongs to.
        atmosphere_component (ForeignKey): A reference to the AtmosphereComponent model, indicating the specific component of the atmosphere.
        percent (FloatField): The percentage of this atmosphere component in the planet's atmosphere.
    Methods:
        __str__(): Returns the name of the atmosphere component.
        clean(): Validates that the sum of 'percent' for the planet in the database does not exceed 100.
    Meta:
        verbose_name (str): Human-readable name for the object.
        verbose_name_plural (str): Human-readable plural name for the object.
        indexes (list): Database indexes for the model.
        constraints (list): Database constraints for the model.
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
    
    def clean(self):
        """
        Checks that the sum of 'percent' for the planet in the database is <= 100
        """
        if self.__class__.objects.filter(planet=self.planet).aggregate(models.Sum('percent', default=0))['percent__sum'] + self.percent > 100:
            raise ValidationError(_('the sum of the percent for the planet cannot be greater than 100'))

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
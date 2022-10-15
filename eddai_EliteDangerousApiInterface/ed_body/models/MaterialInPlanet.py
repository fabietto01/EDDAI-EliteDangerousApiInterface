from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator

from ed_body.models.Planet import Planet
from ed_material.models.Material import Material

class MaterialInPlanet(models.Model):
    """
    mello contenete la relazione tra i materialli e i pianeti
    """
    planet = models.ForeignKey(
        Planet, models.CASCADE,
        verbose_name=_('planet'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )
    material = models.ForeignKey(
        Material, models.PROTECT,
        verbose_name=_('material'),
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

    def clean(self) -> None:
        if self.material.type != Material.MaterialType.RAW.label:
            raise ValidationError(_('the material must be raw'))

    class Meta:
        verbose_name = _('material in planet')
        verbose_name_plural = _('materials in planets')
        indexes = [
            models.Index(fields=['planet', 'material'], name='planet_material_idx'),
        ]
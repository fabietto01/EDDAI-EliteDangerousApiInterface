from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

from ed_body.models.BaseBody import BaseBody
from ed_body.models.StarLuminosity import StarLuminosity
from ed_body.models.StarType import StarType

class Star(BaseBody):
    absoluteMagnitude = models.FloatField(
        verbose_name=_('absolute magnitude'),
        validators=[
            MinValueValidator(0, _('the absolute magnitude cannot be less than 0'))
        ]
    )
    age = models.FloatField(
        verbose_name=_('age'),
        help_text=_('age in millions of years'),
        validators=[
            MinValueValidator(0, _('the age cannot be less than 0'))
        ]
    )
    luminosity = models.ForeignKey(
        StarLuminosity, models.PROTECT,
        verbose_name=_('luminosity'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )
    starType = models.ForeignKey(
        StarType, models.PROTECT,
        verbose_name=_('star type'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )
    stellarMass = models.FloatField(
        verbose_name=_('stellar mass'),
        help_text=_("mass as multiple of Sol's mass"),
        validators=[
            MinValueValidator(0, _('the stellar mass cannot be less than 0'))
        ]
    )
    subclass = models.IntegerField(
        verbose_name=_('subclass'),
        validators=[
            MinValueValidator(0, _('the subclass cannot be less than 0')),
            MaxValueValidator(9, _('the subclass cannot be greater than 9'))
        ]
    )

    class Meta:
        verbose_name = _('star')
        verbose_name_plural = _('stars')
        indexes = [
            models.Index(fields=['luminosity', 'starType'], name='luminosity_starType_idx')
        ]
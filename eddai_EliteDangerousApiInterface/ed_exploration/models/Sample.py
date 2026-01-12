from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from core.models import OwnerAndDateModels

from ed_body.models.Planet import Planet
from ed_exploration.models.SampleSignals import SampleSignals

class Sample(OwnerAndDateModels):
    """
    classe model contente tutti i campioni di un pianeta
    """
    planet = models.ForeignKey(
        Planet, models.CASCADE,
        verbose_name=_('planet'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )
    type = models.ForeignKey(
        SampleSignals, models.PROTECT,
        verbose_name=_('type'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )

    def __str__(self):
        return str(self.type) + ' in ' + str(self.planet)

    def clean(self):
        if Sample.objects.filter(type=self.type, planet=self.planet).exclude(id=self.pk).exists():
            raise ValidationError('Sample with this type already exists in this planet.')

    class Meta:
        verbose_name = _("Sample")
        verbose_name_plural = _("Samples")
        indexes = [
            models.Index(fields=['type', 'planet']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['type', 'planet'], name='sample_unique_type_planet'),
        ]
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from django.core.validators import MinValueValidator

from core.models import OwnerAndDateModels

from ed_body.models.Planet import Planet
from ed_exploration.models.SignalSignals import SignalSignals

class Signal(OwnerAndDateModels):
    """
    classe model contente tutti i segnali di un pianeta
    """
    planet = models.ForeignKey(
        Planet, models.CASCADE,
        verbose_name=_('planet'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )
    type = models.ForeignKey(
        SignalSignals, models.PROTECT,
        verbose_name=_('type'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )
    count = models.IntegerField(
        verbose_name=_('count'),
        help_text=_('number of Signals'),
        validators=[
            MinValueValidator(0, _('the count cannot be less than 0'))
        ],
    )

    def __str__(self):
        return str(self.type) + ' in ' + str(self.planet)

    def clean(self):
        if Signal.objects.filter(type=self.type, planet=self.planet).exclude(id=self.pk).exists():
            raise ValidationError('Signal with this type already exists in this planet.')

    class Meta:
        verbose_name = _("Signals")
        verbose_name_plural = _("Signals")
        ordering = ['type', 'planet']
        indexes = [
            models.Index(fields=['type', 'planet']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['type', 'planet'], name='signal_unique_type_planet'),
        ]
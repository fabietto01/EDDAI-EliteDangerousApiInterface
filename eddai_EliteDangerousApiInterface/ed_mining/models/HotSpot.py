from django.db import models
from django.utils.translation import gettext_lazy as _

from django.core.validators import MaxValueValidator, MinValueValidator

from core.models import OwnerAndDateModels

from .Ring import Ring
from .HotspotType import HotspotType

class HotSpot(OwnerAndDateModels):
    """
    """
    type = models.ForeignKey(
        HotspotType, models.PROTECT,
        verbose_name=_('type'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )
    ring = models.ForeignKey(
        Ring, models.CASCADE, 
        verbose_name=_('ring'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )
    count = models.IntegerField(
        verbose_name=_('count'),
        help_text=_('number of HotSpot'),
        validators=[
            MinValueValidator(0, _('the count cannot be less than 0'))
        ],
    )
    
    def __str__(self):
        return str(self.type) + ' in ' + str(self.ring)

    class Meta:
        verbose_name = _("HotSpot")
        verbose_name_plural = _("HotSpots")
        indexes = [
            models.Index(fields=['type', 'ring']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['type', 'ring'], name='unique_type_ring'),
        ]
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _


from ed_system.models import System

class BaseBody(models.Model):
    """
    modello di base per le informazioni dei corpi celesti
    presenti al interno del systema
    """
    name = models.CharField(
        max_length=255,
        verbose_name=_('name'),
    )
    system = models.ForeignKey(
        System, models.CASCADE,
        verbose_name=_('system'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )
    distance = models.FloatField(
        verbose_name=_('distance'),
        help_text=_('distance from the stary center'),
        validators=[
            MinValueValidator(0, _('the distance cannot be less than 0'))
        ]
    )
    updated = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        verbose_name = _('body')
        verbose_name_plural = _('bodies')
        indexes = [
            models.Index(fields=['system']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['name','system'], name='unique_body_in_system'),
        ]
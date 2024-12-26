from django.db import models
from django.utils.translation import gettext_lazy as _

from eddn.models import AbstractDataEDDN

class State(AbstractDataEDDN, models.Model):
    """
    modello utilizato per memorizzare tutti i tipi di stati per le minori fazioni
    """
    class TypeChoices(models.TextChoices):
        """
        tipi di stato per le minori fazioni
        """
        HAPPINESS = 'H', _('Happiness')
        ECONOMY = 'E', _('Economy')
        SECURITY = 'S', _('Security')
        OTHER = 'O', _('Other')

    name = models.CharField(
        max_length=255,  verbose_name=_('name')
    )
    type = models.CharField(
        max_length=1, choices=TypeChoices.choices,
        default=TypeChoices.OTHER,
        verbose_name=_('type')
    )
    description = models.TextField(
        blank=True, null=True,
        verbose_name=_('description')
    )

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = _('State')
        verbose_name_plural = _('States')
        ordering = ('name',)
        indexes = [
            models.Index(fields=['name', 'type'])
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'type'], 
                name='unique_state_name_type'
            ),
        ]
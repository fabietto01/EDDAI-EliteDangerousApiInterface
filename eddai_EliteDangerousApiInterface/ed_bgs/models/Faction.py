from django.db import models
from django.utils.translation import gettext_lazy as _

from eddn.models import AbstractDataEDDN

def default_faction():
    from core.utility import get_or_none
    return get_or_none(Faction, name='Independent')

class Faction(AbstractDataEDDN, models.Model):

    name = models.CharField(
        max_length=255, unique=True, verbose_name=_('name')
    )
    description = models.TextField(
        blank=True, null=True,
        verbose_name=_('description')
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _('faction')
        verbose_name_plural = _('factions')
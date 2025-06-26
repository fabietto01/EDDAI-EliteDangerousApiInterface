from django.db import models
from django.utils.translation import gettext_lazy as _

from ed_dbsync.models import AbstractDataEDDN

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
    
    @staticmethod
    def get_default():
        ctx, create = Faction.objects.get_or_create(name='Independent')
        return ctx

    class Meta:
        verbose_name = _('faction')
        verbose_name_plural = _('factions')
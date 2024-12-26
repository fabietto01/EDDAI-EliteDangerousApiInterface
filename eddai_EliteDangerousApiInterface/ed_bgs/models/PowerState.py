from django.db import models
from django.utils.translation import gettext_lazy as _

from eddn.models import AbstractDataEDDN

class PowerState(AbstractDataEDDN, models.Model):
    name = models.CharField(
        max_length=255, verbose_name=_('name'),
        unique=True
    )
    description = models.TextField(
        blank=True, null=True,
        verbose_name=_('description')
    )

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = _('State of Power')
        verbose_name_plural = _('States of Power')
        ordering = ('name',)
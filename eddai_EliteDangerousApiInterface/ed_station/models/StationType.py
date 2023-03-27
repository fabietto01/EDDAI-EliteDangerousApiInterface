from django.db import models
from django.utils.translation import gettext_lazy as _

from eddn.models import AbstractDataEDDN

class StationType(AbstractDataEDDN):
    name = models.CharField(
        max_length=100, unique=True, verbose_name=_('name')
    )
    description = models.TextField(
        blank=True, null=True
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _('station type')
        verbose_name_plural = _('station types')
    
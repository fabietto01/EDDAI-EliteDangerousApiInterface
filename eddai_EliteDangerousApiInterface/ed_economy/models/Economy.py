from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from eddn.models import AbstractDataEDDN

class Economy(AbstractDataEDDN, models.Model):

    name = models.CharField(
        max_length=100, unique=True, verbose_name=_('name')
    )
    description = models.TextField(
        blank=True, null=True
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _('economy')
        verbose_name_plural = _('economies')
        ordering = ['name']
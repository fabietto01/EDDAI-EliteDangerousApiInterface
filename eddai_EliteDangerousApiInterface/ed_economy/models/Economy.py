from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from ed_dbsync.models import AbstractDataEDDN

class Economy(AbstractDataEDDN, models.Model):

    name = models.CharField(
        max_length=100, unique=True, verbose_name=_('name')
    )
    description = models.TextField(
        blank=True, null=True
    )

    def __str__(self) -> str:
        return self.name    
    
    @staticmethod
    def get_max_proportion() -> float:
        """Return the maximum proportion value for an economy."""
        return 3.0
    
    @staticmethod
    def get_min_proportion() -> float:
        """Return the minimum proportion value for an economy."""
        return 0.0

    class Meta:
        verbose_name = _('economy')
        verbose_name_plural = _('economies')
        ordering = ['name']
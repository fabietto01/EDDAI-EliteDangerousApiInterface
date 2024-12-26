from django.db import models
from django.utils.translation import gettext_lazy as _

from ed_bgs.models.Faction import Faction

class Power(models.Model):
    
    name = models.CharField(
        max_length=255, unique=True, verbose_name=_('name')
    )
    headquarter = models.OneToOneField(
        'ed_system.System', on_delete=models.PROTECT,
        verbose_name=_('headquarter'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss',
    )
    allegiance = models.ForeignKey(
        Faction, on_delete=models.PROTECT,
        verbose_name=_('allegiance'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss',
    )
    note = models.TextField(
        blank=True, null=True,
        verbose_name=_('note')
    )

    def __str__(self) -> str:
        return str(self.name)

    class Meta:
        verbose_name = _('Power')
        verbose_name_plural = _('Powers')
        ordering = ('name',)
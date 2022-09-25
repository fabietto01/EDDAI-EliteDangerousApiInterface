from django.db import models
from django.utils.translation import gettext_lazy as _

from django.core.exceptions import ValidationError

class PowerInSystem(models.Model):
    """
    modelo corellato 1:1 con il modelo system contente le informazioni
    riguradanti le Power all interno del systema, avra una relazione n:n con
    il modello Power
    """
    MaxRelation = 2
    StateForMoreRellation = ('Contested')

    system = models.OneToOneField(
        'ed_system.System', on_delete=models.CASCADE,
        verbose_name=_('system'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )
    powers = models.ManyToManyField(
        'ed_bgs.Power', verbose_name=_('Powers'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )
    state = models.ForeignKey(
        'ed_bgs.PowerState', on_delete=models.PROTECT,
        verbose_name=_('state'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss',
    )
    updated = models.DateTimeField(
        auto_now=True
    )

    def __str__(self) -> str: 
        return str(self.state) + " by " + " and ".join([str(p.name) for p in self.powers.all()])

    class Meta:
        verbose_name = _('Power in System')
        verbose_name_plural = _('Powers in Systems')
        ordering = ('system',)
        indexes = [
            models.Index(fields=['state']),
        ]

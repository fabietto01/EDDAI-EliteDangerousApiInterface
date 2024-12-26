from django.db import models
from django.utils.translation import gettext_lazy as _

from core.models import OwnerAndDateModels

from .Commodity import Commodity

class CommodityInStation(OwnerAndDateModels):
    """
    modello utilizato per salvare la relazione tra le commodity e
    le stanzione che condengono talle commodity
    """
    station = models.ForeignKey(
        'ed_station.Station', on_delete=models.CASCADE,
        verbose_name=_('station'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )
    commodity = models.ForeignKey(
        Commodity, on_delete=models.CASCADE,
        verbose_name=_('commodity'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )
    buyPrice = models.IntegerField(
        verbose_name=_('buy price'),
        default=0,
        help_text=_('the buy price of the commodity')
    )
    sellPrice = models.IntegerField(
        verbose_name=_('sell price'),
        default=0,
        help_text=_('the sell price of the commodity')
    )
    inStock = models.IntegerField(
        verbose_name=_('stock'),
        default=0,
        help_text=_('the number of units in stock')
    )
    stockBracket = models.IntegerField(
        verbose_name=_('stock bracket'),
        default=0,
        help_text=_('the stock bracket of the commodity')
    )
    demand = models.FloatField(
        verbose_name=_('demand'),
        default=0,
        help_text=_('the demand of the commodity')
    )
    demandBracket = models.IntegerField(
        verbose_name=_('demand bracket'),
        default=0,
        help_text=_('the demand bracket of the commodity')
    )

    def __str__(self) -> str:
        return f'{self.station} - {self.commodity}'

    class Meta:
        verbose_name = _('commodity in station')
        verbose_name_plural = _('commodities in station')
        indexes = [
            models.Index(fields=['station']),
            models.Index(fields=['commodity'])
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['station','commodity'], name='unique_commodity_in_station'
                )
        ]

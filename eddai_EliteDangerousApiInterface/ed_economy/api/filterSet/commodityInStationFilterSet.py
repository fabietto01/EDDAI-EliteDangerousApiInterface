from django_filters import rest_framework

from ed_core.api.filters import BaseDistanceFilterSet

from ed_economy.models import CommodityInStation

class CommodityInStationFilterSet(BaseDistanceFilterSet):
    
    distance_field = 'station__system__coordinate'
    default_ordering = ['station']

    class Meta:
        model = CommodityInStation
        fields = {
            "station__system":['exact',],
            "station":['exact',],
            "commodity":['exact','in'],
            "buyPrice": ['exact','lt', 'gt'],
            "sellPrice": ['exact','lt', 'gt'],
            "inStock":['exact','lt', 'gt'],
            "demand":['exact','lt', 'gt'],
        }

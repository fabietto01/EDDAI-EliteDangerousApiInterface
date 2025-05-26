import django_filters

from ed_core.api.filters import BaseDistanceFilterSet
from ed_station.models import Station, Service

class StationFilterSet(BaseDistanceFilterSet):

    distance_field = "system__coordinate"
    default_ordering = "name"

    class Meta:
        model = Station
        fields = {
            'system': ['exact',],
            'landingPad': ['exact'],
            'primaryEconomy': ['in'],
            'secondaryEconomy': ['in'],
            'minorFaction': ['in',],
            'service': ['exact','in'],
            'distance': ['lt', 'gt']
        }
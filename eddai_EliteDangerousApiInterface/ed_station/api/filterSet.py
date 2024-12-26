import django_filters
from ed_station.models import Station
from ed_system.models import System
from django.db.models import F

from ed_core.functions import Distanza3D

class StationFilterSet(django_filters.FilterSet):

    @staticmethod
    def filter_by_system(queryset, name, value):
        system:System = System.objects.get(id=value)
        return queryset.annotate(
            distance_st=Distanza3D(F('system__coordinate'), point=system.coordinate)
        ).order_by('distance_st')
    
    order_by_system = django_filters.NumberFilter(
        method='filter_by_system',
        label='from system',
        distinct=True
    )

    class Meta:
        model = Station
        fields = {
            'system': ['exact',],
            'landingPad': ['exact'],
            'primaryEconomy': ['in'],
            'secondaryEconomy': ['in'],
            'minorFaction': ['in',],
            'service': ['in',],
            'commodity': ['in',],
            'distance': ['lt', 'gt']
        }
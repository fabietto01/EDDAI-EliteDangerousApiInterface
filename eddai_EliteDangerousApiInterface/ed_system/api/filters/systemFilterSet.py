import django_filters
from ed_system.models import System
from django.db.models import F

from ed_core.functions import Distanza3D

class SystemFilterSet(django_filters.FilterSet):
    """
    filter for system model
    """
    @staticmethod
    def filter_by_system(queryset, name, value:System):
        return queryset.annotate(
            distance_st=Distanza3D(
                F('coordinate'),
                point=value.coordinate
            )
        ).order_by('distance_st')

    order_by_system = django_filters.ModelChoiceFilter(
        queryset=System.objects.all(),
        method='filter_by_system',
        label='from system',
        distinct=True
    )

    class Meta:
        model = System
        fields = {
            'security': ['exact',],
            'population': ['exact', 'lt', 'gt'],
            'primaryEconomy': ['exact',],
            'secondaryEconomy': ['exact',],
            'conrollingFaction': ['exact',],
        }
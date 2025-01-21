import django_filters
from django.db.models import F

from ed_core.functions import Distanza3D

from ed_body.models import BaseBody
from ed_system.models import System

class BaseBodyFilterSet(django_filters.FilterSet):

    def __init__(self, param=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.data.get('order_by_system'):
            self.filters.pop('order_by_distance_st', None)

    @staticmethod
    def filter_by_system(queryset, name, value:System):
        return queryset.annotate(
            distance_st=Distanza3D(
                F('system__coordinate'),
                point=value.coordinate
            )
        )
    
    order_by_system = django_filters.ModelChoiceFilter(
        queryset=System.objects.all(),
        method='filter_by_system',
        label='from system',
        distinct=True
    )

    order_by_distance_st = django_filters.OrderingFilter(
        fields=(
            ('distance_st', 'distance_st'),
        ),
        initial='distance_st'
    )

    class Meta:
        model = BaseBody
        fields = {
            'name': ['exact'],
            'system': ['exact'],
            'distance': ['lt', 'lte', 'gt', 'gte'],
        }
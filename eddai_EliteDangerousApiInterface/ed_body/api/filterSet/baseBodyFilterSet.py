import django_filters
from django.db.models import F

from ed_core.functions import Distanza3D

from ed_body.models import BaseBody
from ed_system.models import System


class BaseBodyFilterSet(django_filters.FilterSet):

    @staticmethod
    def filter_by_system(queryset, name, value:System):
        return queryset.annotate(
            distance_st=Distanza3D(
                F('system__coordinate'),
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
        model = BaseBody
        fields = {
            'name': ['exact'],
            'system': ['exact'],
            'distance': ['lt', 'lte', 'gt', 'gte'],
        }
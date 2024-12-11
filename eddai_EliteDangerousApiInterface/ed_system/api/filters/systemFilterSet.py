import django_filters
from ed_system.models import System

from django.db.models.expressions import RawSQL
from django.db.models import FloatField

class SystemFilterSet(django_filters.FilterSet):
    """
    filter for system model
    """
    @staticmethod
    def filter_by_system(queryset, name, value):
        system:System = System.objects.get(id=value)
        x, y, z, srid = system.coordinate.x, system.coordinate.y, system.coordinate.z, system.coordinate.srid
        return queryset.annotate(
            distance=RawSQL(
                "ST_3DDistance(coordinate, ST_GeomFromText('POINT(%s %s %s)', %s))",
                (x, y, z, srid),
                output_field=FloatField()
            )
        ).order_by('distance')

    order_by_system = django_filters.NumberFilter(
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
import django_filters
from django.db.models import QuerySet

from django.db.models import F
from ed_core.functions import Distanza3D
from .castomOrderingFilter import OrderingFilterOrDefault
from ed_system.models import System

class BaseDistanceFilterSet(django_filters.FilterSet):
    """
    BaseDistanceFilterSet is a custom filter set for filtering and ordering querysets based on distance.
    Attributes:
        distance_field (str): The field used to calculate distance. Must be defined in subclasses.
        default_ordering (list[str]): The default ordering for the queryset. Must be defined in subclasses.
        order_by_system (django_filters.ModelChoiceFilter): A filter for selecting a system to order by distance.
        order_by_system_distance (OrderingFilterOrDefault): A filter for ordering by distance with a default ordering.
    Methods:
        get_default_ordering() -> list[str]:
            Returns the default ordering for the queryset. Raises ValueError if not defined.
        get_distance_field():
            Returns the distance field. Raises ValueError if not defined.
        _has_ordering(queryset: QuerySet) -> bool:
            Checks if the queryset has any ordering applied.
        __init__(*args, **kwargs):
            Initializes the filter set and removes 'order_by_system_distance' filter if 'order_by_system' is not in the data.
        filter_queryset(queryset):
            Filters the queryset and applies default ordering if no ordering is present.
        filter_by_distance(queryset, name, value):
            Annotates the queryset with a calculated distance field based on the provided system coordinates.
    """

    distance_field = None
    default_ordering = None

    def get_default_ordering(self) -> list[str]:
        if self.default_ordering is None:
            raise ValueError('default_ordering is not defined')
        if isinstance(self.default_ordering, str):
            return [self.default_ordering]
        return self.default_ordering

    def get_distance_field(self):
        if self.distance_field is None:
            raise ValueError('distance_field is not defined')
        return self.distance_field
    
    def _has_ordering(self, queryset: QuerySet) -> bool:
        return bool(queryset.query.order_by)
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.data.get('order_by_system'):
            self.filters.pop('order_by_system_distance', None)

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        if not self._has_ordering(queryset):
            queryset = queryset.order_by(*self.get_default_ordering())
        return queryset

    def filter_by_distance(self, queryset, name, value):
        return queryset.annotate(
            distance_st=Distanza3D(
                F(self.get_distance_field()),
                point=value.coordinate
            )
        )
    
    order_by_system = django_filters.ModelChoiceFilter(
        queryset=System.objects.all(),
        method='filter_by_distance',
        label='from system',
        distinct=True
    )
    
    order_by_system_distance = OrderingFilterOrDefault(
        fields=(
            ('distance_st', 'distance_st'),
        ),
        initial='distance',
        default_ordering=['distance_st']
    )
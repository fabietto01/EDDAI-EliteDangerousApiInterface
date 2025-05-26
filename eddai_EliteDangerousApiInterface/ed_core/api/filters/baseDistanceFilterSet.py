import django_filters
from django.db.models import QuerySet
from django.utils.translation import gettext_lazy as _

from django.db.models import F
from django.db.models.functions import Round
from ed_core.functions import Distanza3D
from .castomOrderingFilter import OrderingFilterOrDefault
from ed_system.models import System

from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

class BaseDistanceFilterSet(django_filters.FilterSet):
    """
    BaseDistanceFilterSet is a custom filter set class that extends `django_filters.FilterSet`.
    It provides filtering and ordering functionality based on distance calculations.
    Attributes:
        distance_field (str): The name of the field used for distance calculations. Must be defined in subclasses.
        default_ordering (list[str] or str): The default ordering for the queryset. Must be defined in subclasses.
    Methods:
        get_default_ordering() -> list[str]:
            Returns the default ordering as a list. Raises a ValueError if `default_ordering` is not defined.
        get_distance_field():
            Returns the distance field. Raises a ValueError if `distance_field` is not defined.
        _has_ordering(queryset: QuerySet) -> bool:
            Checks if the given queryset has any ordering applied.
        __init__(*args, **kwargs):
            Initializes the filter set. Removes distance-related filters if `distance_by_system` is not present in the data.
        filter_queryset(queryset):
            Filters and orders the queryset based on the provided filters and default ordering.
            If `distance_by_system` is provided but no range filters (`filter_distance_by_system__lt` or `filter_distance_by_system__gt`)
            are specified, it defaults to filtering distances less than 200.
        filter_by_distance(queryset, name, value):
            Annotates the queryset with a calculated distance field (`distance_st`) based on the provided system's coordinates.
    Filters:
        distance_by_system:
            A `ModelChoiceFilter` that allows filtering by a specific system. Uses the `filter_by_distance` method.
        order_distance_by_system:
            An `OrderingFilterOrDefault` that allows ordering by the calculated distance field (`distance_st`).
            Defaults to ordering by distance.
        filter_distance_by_system__lt:
            A `NumberFilter` that filters systems with distances less than the specified value.
        filter_distance_by_system__gt:
            A `NumberFilter` that filters systems with distances greater than the specified value.
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
        if not self.data.get('distance_by_system'):
            self.filters.pop('order_distance_by_system', None)
            self.filters.pop('filter_distance_by_system__lt', None)
            self.filters.pop('filter_distance_by_system__gt', None)

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)
        if not self._has_ordering(queryset):
            queryset = queryset.order_by(*self.get_default_ordering())
        if self.data.get('distance_by_system'):
            if not ( self.data.get('filter_distance_by_system__lt') or self.data.get('filter_distance_by_system__gt') ):
                queryset = queryset.filter(distance_st__lt=200)
        return queryset

    @extend_schema_field(OpenApiTypes.INT)
    def filter_by_distance(self, queryset, name, value):
        return queryset.annotate(
            distance_st=Round(
                Distanza3D(
                    F(self.get_distance_field()),
                    point=value.coordinate
                ),
                3
            )
        )
        
    distance_by_system = django_filters.ModelChoiceFilter(
        queryset=System.objects.all(),
        method='filter_by_distance',
        label=_('From system'),
    )
    
    order_distance_by_system = OrderingFilterOrDefault(
        fields=(
            ('distance_st', 'distance_st'),
        ),
        initial='distance',
        default_ordering=['distance_st'],
        label=_('Order by distance'),
    )
    
    filter_distance_by_system__lt = django_filters.NumberFilter(
        field_name='distance_st',
        lookup_expr='lt',
        label=_('Distance less than'),
    )

    filter_distance_by_system__gt = django_filters.NumberFilter(
        field_name='distance_st',
        lookup_expr='gt',
        label=_('Distance greater than'),
    )
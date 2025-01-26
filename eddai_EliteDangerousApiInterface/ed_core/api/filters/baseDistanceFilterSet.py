import django_filters


from django.db.models import F
from ed_core.functions import Distanza3D
from .castomOrderingFilter import OrderingFilterOrDefault
from ed_system.models import System

class BaseDistanceFilterSet(django_filters.FilterSet):
    """
    BaseDistanceFilterSet is a custom filter set for filtering and ordering querysets based on distance.
    Attributes:
        distance_field (str): The name of the field representing the distance. Must be defined in subclasses.
    Methods:
        get_distance_field():
            Returns the distance field name. Raises ValueError if distance_field is not defined.
        __init__(*args, **kwargs):
            Initializes the filter set. Removes 'order_by_distance' filter if 'order_by_system' is not present in the data.
        filter_by_distance(queryset, name, value):
            Filters the queryset by annotating it with a calculated distance using the provided coordinate.
    Filters:
        order_by_system (django_filters.ModelChoiceFilter):
            Filters the queryset based on the selected system and applies the distance filter method.
        order_by_distance (OrderingFilterOrDefault):
            Orders the queryset by the annotated distance field 'distance_st'.
    """

    distance_field = None

    def get_distance_field(self):
        if self.distance_field is None:
            raise ValueError('distance_field is not defined')
        return self.distance_field
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.data.get('order_by_system'):
            self.filters.pop('order_by_distance', None)

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
    
    order_by_distance = OrderingFilterOrDefault(
        fields=(
            ('distance_st', 'distance_st'),
        ),
        initial='distance',
        default_ordering=['distance_st']
    )
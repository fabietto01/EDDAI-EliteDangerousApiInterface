from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from ed_core.api.mixins import DistanceModelMixin
from django.utils.translation import gettext_lazy as _

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from ..filterSet import BaseBodyFilterSet
from ..serializers import BaseBodySerializer, BaseBodyDistanceSerializer

from ed_body.models import BaseBody

from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes
)

@extend_schema_view(
    list=extend_schema(
        description=_("Returns a list of celestial bodies, including both planets and stars."),
        parameters=[
            OpenApiParameter(name='name', description=_("Filter by the name of the body."), required=False, type=OpenApiTypes.STR),
            OpenApiParameter(name='name__startswith', description=_("Filter bodies whose names start with the specified string."), required=False, type=OpenApiTypes.STR),
            OpenApiParameter(name='system', description=_("Filters based on the system ID of the body. this filter disables the possibility of calculating distances between systemi"), required=False, type=OpenApiTypes.INT64),
            OpenApiParameter(name='distance__gt', description=_("Filter bodies whose distance is greater than the specified value."), required=False, type=OpenApiTypes.FLOAT),
            OpenApiParameter(name='distance__gte', description=_("Filter bodies whose distance is greater than or equal to the specified value."), required=False, type=OpenApiTypes.FLOAT),
            OpenApiParameter(name='distance__lt', description=_("Filter bodies whose distance is less than the specified value."), required=False, type=OpenApiTypes.FLOAT),
            OpenApiParameter(name='distance__lte', description=_("Filter bodies whose distance is less than or equal to the specified value."), required=False, type=OpenApiTypes.FLOAT),
            OpenApiParameter(name='ordering_body', description=_("Sorts the bodies in the system according to their hierarchy in the system, filter only works if passed in conteporanium with system"), required=False, type=OpenApiTypes.BOOL),
        ]
    ),
)
class BaseBodyViewSet(DistanceModelMixin, ListModelMixin, GenericViewSet):
    """
    BaseBodyViewSet is a view set that provides list and retrieve actions for the BaseBody model.
    Attributes:
        queryset (QuerySet): A queryset that retrieves all BaseBody objects, selecting related 'star' and 'planet' objects.
        serializer_class (Serializer): The serializer class used to serialize and deserialize BaseBody instances.
        filterset_class (FilterSet): The filter set class used to filter the queryset.
        filter_backends (list): A list of filter backends used to filter the queryset.
        search_fields (list): A list of fields that can be searched using the search filter backend.
    """
    
    queryset = BaseBody.objects.all().select_related("star", "planet")
    serializer_class = BaseBodySerializer
    distance_serializer_class = BaseBodyDistanceSerializer
    filter_param_distance = 'distance_by_system'
    filterset_class = BaseBodyFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']

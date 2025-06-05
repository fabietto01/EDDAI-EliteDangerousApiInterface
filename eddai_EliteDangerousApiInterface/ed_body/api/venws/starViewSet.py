from core.api.viewsets import OwnerAndDateModelViewSet
from ed_core.api.mixins import DistanceModelMixin
from django.utils.translation import gettext_lazy as _

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from ..serializers import StarSerializer, StarDistanceSerializer
from ..filterSet import StarFilterSet

from ed_body.models import Star

from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes
)

@extend_schema_view(
    list=extend_schema(
        description=_("Returns a list of stars only."),
        parameters=[
            OpenApiParameter(name='name', description=_("Filter by the name of the body."), required=False, type=OpenApiTypes.STR),
            OpenApiParameter(name='name__startswith', description=_("Filter bodies whose names start with the specified string."), required=False, type=OpenApiTypes.STR),
            OpenApiParameter(name='system', description=_("Filters based on the system ID of the body. this filter disables the possibility of calculating distances between systemi"), required=False, type=OpenApiTypes.INT64),
            OpenApiParameter(name='distance__gt', description=_("Filter bodies whose distance is greater than the specified value."), required=False, type=OpenApiTypes.FLOAT),
            OpenApiParameter(name='distance__gte', description=_("Filter bodies whose distance is greater than or equal to the specified value."), required=False, type=OpenApiTypes.FLOAT),
            OpenApiParameter(name='distance__lt', description=_("Filter bodies whose distance is less than the specified value."), required=False, type=OpenApiTypes.FLOAT),
            OpenApiParameter(name='distance__lte', description=_("Filter bodies whose distance is less than or equal to the specified value."), required=False, type=OpenApiTypes.FLOAT),
            OpenApiParameter(name='ordering_body', description=_("Sorts the bodies in the system according to their hierarchy in the system, filter only works if passed in conteporanium with system"), required=False, type=OpenApiTypes.BOOL),
            OpenApiParameter(name='luminosity', description=_("Filter by the luminosity of the star."), required=False, type=OpenApiTypes.INT64),
            OpenApiParameter(name='starType', description=_("Filter by the type of the star."), required=False, type=OpenApiTypes.INT64),
        ]
    ),
    retrieve=extend_schema(description="Returns the details of the star."),
    create=extend_schema(description="Creates a new star object."),
    update=extend_schema(description="Updates an existing star object."),
    partial_update=extend_schema(description="Partially updates an existing star object."),
    destroy=extend_schema(description="Deletes an existing star object.")
)
class StarViewSet(DistanceModelMixin, OwnerAndDateModelViewSet):
    """
    StarViewSet is a view set for handling API requests related to the Star model.
    Attributes:
        queryset (QuerySet): A queryset containing all Star objects.
        serializer_class (Serializer): The serializer class used for Star objects.
        filter_backends (list): A list of filter backends used for filtering the queryset.
        search_fields (list): A list of fields that can be searched using the search filter.
    """
    
    queryset = Star.objects.all()
    serializer_class = StarSerializer
    distance_serializer_class = StarDistanceSerializer
    filter_param_distance = 'distance_by_system'
    filterset_class = StarFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
from core.api.viewsets import OwnerAndDateModelViewSet
from ed_core.api.mixins import DistanceModelMixin
from django.utils.translation import gettext_lazy as _

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from ..serializers import PlanetSerializer, PlanetDistanceSerializer
from ..filterSet import PlanetFilterSet

from ed_body.models import Planet

from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes
)

@extend_schema_view(
    list=extend_schema(
        description=_("Returns a list of planets."),
        parameters=[
            OpenApiParameter(name='name', description=_("Filter by the name of the body."), required=False, type=OpenApiTypes.STR),
            OpenApiParameter(name='name__startswith', description=_("Filter bodies whose names start with the specified string."), required=False, type=OpenApiTypes.STR),
            OpenApiParameter(name='system', description=_("Filters based on the system ID of the body. this filter disables the possibility of calculating distances between systemi"), required=False, type=OpenApiTypes.INT64),
            OpenApiParameter(name='distance__gt', description=_("Filter bodies whose distance is greater than the specified value."), required=False, type=OpenApiTypes.FLOAT),
            OpenApiParameter(name='distance__gte', description=_("Filter bodies whose distance is greater than or equal to the specified value."), required=False, type=OpenApiTypes.FLOAT),
            OpenApiParameter(name='distance__lt', description=_("Filter bodies whose distance is less than the specified value."), required=False, type=OpenApiTypes.FLOAT),
            OpenApiParameter(name='distance__lte', description=_("Filter bodies whose distance is less than or equal to the specified value."), required=False, type=OpenApiTypes.FLOAT),
            OpenApiParameter(name='ordering_body', description=_("Sorts the bodies in the system according to their hierarchy in the system, filter only works if passed in conteporanium with system"), required=False, type=OpenApiTypes.BOOL),
            OpenApiParameter(name='atmosphereType', description=_("Filter by the type of atmosphere present on the planet."), required=False, type=OpenApiTypes.INT64),
            OpenApiParameter(name='planetType', description=_("Filter by the type of planet."), required=False, type=OpenApiTypes.INT64),
            OpenApiParameter(name='volcanism', description=_("Filter by the type of volcanism present on the planet."), required=False, type=OpenApiTypes.INT64),
            OpenApiParameter(name='terraformState', description=_("Filter by the state of terraforming on the planet."), required=False, type=OpenApiTypes.STR, enum=Planet.TerraformingState.values),
            OpenApiParameter(name='landable', description=_("Filter by whether the planet is landable."), required=False, type=OpenApiTypes.BOOL),
            OpenApiParameter(name='reserveLevel', description=_("Filter by the reserve level of the planet."), required=False, type=OpenApiTypes.STR, enum=Planet.ReserveLevel.values),
        ]   
    ),
    retrieve=extend_schema(description="Returns the details of the planet."),
    create=extend_schema(description="Creates a new planet object."),
    update=extend_schema(description="Updates an existing planet object."),
    partial_update=extend_schema(description="Partially updates an existing planet object."),
    destroy=extend_schema(description="Deletes an existing planet object.")
)
class PlanetViewSet(DistanceModelMixin, OwnerAndDateModelViewSet):
    """
    PlanetViewSet is a view set for handling API requests related to Planet objects.
    Inherits from:
        OwnerAndDateModelViewSet: A custom view set that includes owner and date information.
    Attributes:
        queryset (QuerySet): A Django QuerySet that retrieves all Planet objects.
        serializer_class (Serializer): The serializer class used to convert Planet objects to and from JSON.
        filter_backends (list): A list of filter backends used to filter and search the queryset.
        search_fields (list): A list of fields that can be searched using the search filter backend.
    """
    
    queryset = Planet.objects.select_related(
        'system',
        'atmosphereType',
        'planetType',
        'volcanism',
        'created_by',
        'updated_by'
    ).prefetch_related(
        'ed_body_atmospherecomponentinplanet_related__atmosphere_component'
    )
    serializer_class = PlanetSerializer
    distance_serializer_class = PlanetDistanceSerializer
    filter_param_distance = 'distance_by_system'
    filterset_class = PlanetFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
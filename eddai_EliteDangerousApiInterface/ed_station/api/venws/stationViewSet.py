from core.api.viewsets import OwnerAndDateModelViewSet
from ed_core.api.mixins import DistanceModelMixin
from django.utils.translation import gettext_lazy as _

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from ..serializers import StationSerializer, StationDistanceSerializer
from ..filterSet import StationFilterSet

from ed_station.models import Station

from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes
)

@extend_schema_view(
    list=extend_schema(
        description=_("Returns a list of stations."),
        parameters=[
            OpenApiParameter(name='name', description=_("Filter stations by their name."), required=False, type=OpenApiTypes.STR),
            OpenApiParameter(name='system', description=_("Filter stations by the system ID they belong to."), required=False, type=OpenApiTypes.INT64),
            OpenApiParameter(name='landingPad', description=_("Filter stations by the type of landing pad they have."), required=False, type=OpenApiTypes.STR, enum=Station.LandingPadChoices.values),
            OpenApiParameter(name='primaryEconomy', description=_("Filter stations by their primary economy."), required=False, type=OpenApiTypes.STR),
            OpenApiParameter(name='secondaryEconomy', description=_("Filter stations by their secondary economy."), required=False, type=OpenApiTypes.STR),
            OpenApiParameter(name='minorFaction', description=_("Filter stations by the minor faction they belong to."), required=False, type=OpenApiTypes.INT64),
            OpenApiParameter(name='minorFaction__in', description=_("Filter stations by multiple minor factions."), required=False, type=OpenApiTypes.INT64),
            OpenApiParameter(name='service', description=_("Filter stations by the services they provide."), required=False, type=OpenApiTypes.STR),
            OpenApiParameter(name='service__in', description=_("Filter stations by multiple services they provide."), required=False, type=OpenApiTypes.INT64),
            OpenApiParameter(name='distance__lt', description=_("Filter stations by distance less than the specified value."), required=False, type=OpenApiTypes.FLOAT),
            OpenApiParameter(name='distance__gt', description=_("Filter stations by distance greater than the specified value."), required=False, type=OpenApiTypes.FLOAT),
        ]
    ),
    retrieve=extend_schema(description=_("Returns the details of a station by ID")),
    create=extend_schema(description=_("Creates a new station object.")),
    update=extend_schema(description=_("Updates an existing station object.")),
    partial_update=extend_schema(description=_("Partially updates an existing station object.")),
    destroy=extend_schema(description=_("Deletes an existing station object."))
)
class StationViewSet(DistanceModelMixin, OwnerAndDateModelViewSet):
    
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    distance_serializer_class = StationDistanceSerializer
    filter_param_distance = "distance_by_system"
    filterset_class = StationFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
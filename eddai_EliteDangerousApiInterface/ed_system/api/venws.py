from core.api.viewsets import OwnerAndDateModelViewSet
from ed_core.api.mixins import DistanceModelMixin
from django.utils.translation import gettext_lazy as _

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import SystemSerializer, SystemDistanceSerializer
from .filters import SystemFilterSet

from ed_system.models import System

from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes
)

@extend_schema_view(
    list=extend_schema(
        description=_("Returns a list of systems."),
        parameters=[
            OpenApiParameter(name='search', description=_("Search for systems by name or address."), required=False, type=OpenApiTypes.STR),
            OpenApiParameter(name='security', description=_("Filter by the security level of the system."), required=False, type=OpenApiTypes.STR),
            OpenApiParameter(name='population', description=_("Filter by the population of the system."), required=False, type=OpenApiTypes.INT64),
            OpenApiParameter(name='population__gt', description=_("Filter systems with population greater than the specified value."), required=False, type=OpenApiTypes.INT64),
            OpenApiParameter(name='population__lt', description=_("Filter systems with population greater than or equal to the specified value."), required=False, type=OpenApiTypes.INT64),
            OpenApiParameter(name='primaryEconomy', description=_("Filter by the primary economy of the system."), required=False, type=OpenApiTypes.INT64),
            OpenApiParameter(name='secondaryEconomy', description=_("Filter by the secondary economy of the system."), required=False, type=OpenApiTypes.INT64),
            OpenApiParameter(name='primaryEconomy__in', description=_("Filter systems by a list of primary economies."), required=False, type=OpenApiTypes.INT64),
            OpenApiParameter(name='secondaryEconomy__in', description=_("Filter systems by a list of secondary economies."), required=False, type=OpenApiTypes.INT64),
            OpenApiParameter(name='conrollingFaction', description=_("Filter by the controlling faction of the system."), required=False, type=OpenApiTypes.INT64),
            OpenApiParameter(name='conrollingFaction__in', description=_("Filter systems by a list of controlling factions."), required=False, type=OpenApiTypes.INT64),
            OpenApiParameter(name='created_at', description=_("Filter systems created after the specified date."), required=False, type=OpenApiTypes.DATETIME),
            OpenApiParameter(name='created_at__lt', description=_("Filter systems created after the specified date."), required=False, type=OpenApiTypes.DATETIME),
            OpenApiParameter(name='created_at__gt', description=_("Filter systems created after the specified date."), required=False, type=OpenApiTypes.DATETIME),
            OpenApiParameter(name='updated_at', description=_("Filter systems updated after the specified date."), required=False, type=OpenApiTypes.DATETIME),
            OpenApiParameter(name='updated_at__lt', description=_("Filter systems updated after the specified date."), required=False, type=OpenApiTypes.DATETIME),
            OpenApiParameter(name='updated_at__gt', description=_("Filter systems updated after the specified date."), required=False, type=OpenApiTypes.DATETIME),
            OpenApiParameter(name='conrollingFaction__not', description=_("Exclude systems controlled by the specified faction."), required=False, type=OpenApiTypes.INT64),
            OpenApiParameter(name='conrollingFaction__state', description=_("Filter systems by the state of the controlling faction."), required=False, type=OpenApiTypes.INT64),
            OpenApiParameter(name='conrollingFaction__not__state', description=_("Exclude systems by the state of the controlling faction."), required=False, type=OpenApiTypes.INT64),
            OpenApiParameter(name='conrollingFaction__in__state', description=_("Filter systems by the state of the controlling faction."), required=False, type=OpenApiTypes.INT64),
            OpenApiParameter(name='conrollingFaction__not__in__state', description=_("Exclude systems by the state of the controlling faction."), required=False, type=OpenApiTypes.INT64),
            OpenApiParameter(name='power', description=_("Filter systems by the power that controls them."), required=False, type=OpenApiTypes.INT64),
            OpenApiParameter(name='allegiance', description=_("Filter systems by the allegiance of the controlling faction."), required=False, type=OpenApiTypes.INT64),
            OpenApiParameter(name='government', description=_("Filter systems by the type of government in control."), required=False, type=OpenApiTypes.INT64),
        ]
    ),
    retrieve=extend_schema(description="Returns the details of a system."),
    create=extend_schema(description="Creates a new system object."),
    update=extend_schema(description="Updates an existing system object."),
    partial_update=extend_schema(description="Partially updates an existing system object."),
    destroy=extend_schema(description="Deletes an existing system object.")
)
class SystemViewSet(DistanceModelMixin, OwnerAndDateModelViewSet):
    """
    Handles requests related to systems.
    """
    queryset = System.objects.all()
    serializer_class = SystemSerializer
    distance_serializer_class = SystemDistanceSerializer
    filter_param_distance = 'distance_by_system'
    filterset_class = SystemFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name', 'address']
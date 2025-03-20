from core.api.viewsets import OwnerAndDateModelViewSet
from ed_core.api.mixins import DistanceModelMixin

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import SystemSerializer, SystemDistanceSerializer
from .filters import SystemFilterSet

from ed_system.models import System

from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(
        description="Returns a list of systems, if the parameter distance_by_system is passed,\
            it returns the distance between systems in the distance_st field",
        responses={200: SystemDistanceSerializer(many=True)}
    ),
    retrieve=extend_schema(description="Returns the details of a system by ID"),
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
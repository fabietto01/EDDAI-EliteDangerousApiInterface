from core.api.viewsets import OwnerAndDateModelViewSet
from ed_core.api.mixins import DistanceModelMixin

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import SystemSerializer, SystemDistanceSerializer
from .filters import SystemFilterSet

from ed_system.models import System

from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(description="Returns a list of systems"),
    retrieve=extend_schema(description="Returns the details of a system by ID"),
    create=extend_schema(exclude=True), 
    update=extend_schema(exclude=True), 
    partial_update=extend_schema(exclude=True), 
    destroy=extend_schema(exclude=True)
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
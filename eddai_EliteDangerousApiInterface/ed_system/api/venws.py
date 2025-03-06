from core.api.viewsets import OwnerAndDateModelViewSet
from ed_core.api.mixins import DistanceModelMixin

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import SystemSerializer, SystemDistanceSerializer
from .filters import SystemFilterSet

from ed_system.models import System

class SystemViewSet(DistanceModelMixin, OwnerAndDateModelViewSet):
    """
    
    """
    queryset = System.objects.all()
    serializer_class = SystemSerializer
    distance_serializer_class = SystemDistanceSerializer
    filter_param_distance = 'distance_by_system'
    filterset_class = SystemFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
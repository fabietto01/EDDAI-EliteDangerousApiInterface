from core.api.viewsets import OwnerAndDateModelViewSet
from ed_core.api.mixins import DistanceModelMixin

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from ..serializers import StationSerializer, StationDistanceSerializer
from ..filterSet import StationFilterSet

from ed_station.models import Station

class StationViewSet(DistanceModelMixin, OwnerAndDateModelViewSet):
    
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    distance_serializer_class = StationDistanceSerializer
    filter_param_distance = "distance_by_system"
    filterset_class = StationFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
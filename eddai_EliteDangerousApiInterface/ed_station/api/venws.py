from core.api.viewsets import OwnerAndDateModelViewSet

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import StationSerializer, StationDistanceSerializer
from .filterSet import StationFilterSet

from ed_station.models import Station

class StationViewSet(OwnerAndDateModelViewSet):
    
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    filterset_class = StationFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.request.query_params.get('order_by_system'):
            return StationDistanceSerializer 
        return StationSerializer
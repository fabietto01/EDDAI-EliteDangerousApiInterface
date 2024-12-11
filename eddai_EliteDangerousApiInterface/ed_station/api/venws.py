from rest_framework import viewsets
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend

from .serializers.StationSerializer import StationSerializer

from ed_station.models import Station

class StationViewSet(viewsets.ModelViewSet):
    
    queryset = Station.objects.all()
    serializer_class = StationSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    
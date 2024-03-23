from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from ed_station.api.serializers import StationModelSerializes
from ed_station.models import Station

class StationviewSet(viewsets.ModelViewSet):
    """
    ViewSet dedicato alla visualizzazione di stazioni
    """
    queryset = Station.objects.all()
    serializer_class = StationModelSerializes
    filterset_fields = ['name', "service__id"]
    permission_classes = [IsAuthenticatedOrReadOnly]
from rest_framework import viewsets
from core.api.permissions import IsAdminUserOrReadOnly

from ed_station.api.serializers import StationTypeModelSerializes

from ed_station.models import StationType

class StationTypeViewSet(viewsets.ModelViewSet):
    
    queryset = StationType.objects.all()
    serializer_class = StationTypeModelSerializes
    filterset_fields = ['name']
    permission_classes = [IsAdminUserOrReadOnly]

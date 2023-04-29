from rest_framework import viewsets
from core.api.permissions import IsAdminUserOrReadOnly

from ed_station.api.serializers import ServiceModelSerializes

from ed_station.models import Service


class ServiceViewSet(viewsets.ModelViewSet):

    queryset = Service.objects.all()
    serializer_class = ServiceModelSerializes
    filterset_fields = ['name']
    permission_classes = [IsAdminUserOrReadOnly]
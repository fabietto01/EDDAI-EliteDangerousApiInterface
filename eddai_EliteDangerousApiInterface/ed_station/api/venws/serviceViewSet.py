from rest_framework.viewsets import ReadOnlyModelViewSet

from rest_framework.filters import SearchFilter

from ..serializers import CompactedServiceSerializer, ServiceSerializer
from ed_station.models import Service

class ServiceViewSet(ReadOnlyModelViewSet):
    """
    ServiceViewSet is a viewset for handling CRUD operations on the Service model.
    Attributes:
        queryset (QuerySet): A queryset of all Service objects.
        serializer_class (type): The serializer class used for serializing and deserializing the model.
    """
    
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return CompactedServiceSerializer
        return super().get_serializer_class()
from rest_framework.viewsets import ReadOnlyModelViewSet

from rest_framework.filters import SearchFilter

from ..serializers import PlanetTypeSerializer, CompactedPlanetTypeSerializer
from ed_body.models import PlanetType

class PlanetTypeViewSet(ReadOnlyModelViewSet):
    """
    PlanetTypeViewSet is a viewset for handling CRUD operations on the PlanetType model.
    Attributes:
        queryset (QuerySet): A queryset of all PlanetType objects.
        serializer_class (type): The serializer class used for serializing and deserializing the model.
    """
    
    queryset = PlanetType.objects.all()
    serializer_class = PlanetTypeSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return CompactedPlanetTypeSerializer
        return super().get_serializer_class()
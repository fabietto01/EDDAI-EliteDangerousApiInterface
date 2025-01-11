from rest_framework.viewsets import ReadOnlyModelViewSet

from rest_framework.filters import SearchFilter

from ..serializers import AtmosphereTypeSerializer, CompactedAtmosphereTypeSerializer
from ed_body.models import AtmosphereType

class AtmosphereTypeViewSet(ReadOnlyModelViewSet):
    """
    AtmosphereTypeViewSet is a viewset for handling CRUD operations on the AtmosphereType model.
    Attributes:
        queryset (QuerySet): A queryset of all AtmosphereType objects.
        serializer_class (type): The serializer class used for serializing and deserializing the model.
    """
    queryset = AtmosphereType.objects.all()
    serializer_class = AtmosphereTypeSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return CompactedAtmosphereTypeSerializer
        return super().get_serializer_class()

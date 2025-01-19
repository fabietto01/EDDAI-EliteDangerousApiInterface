from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter

from ..serializers import VolcanismSerializer, CompactedVolcanismSerializer
from ed_body.models import Volcanism

class VolcanismViewSet(ReadOnlyModelViewSet):
    """
    VolcanismViewSet is a viewset for handling CRUD operations on the Volcanism model.
    Attributes:
        queryset (QuerySet): A queryset of all Volcanism objects.
        serializer_class (type): The serializer class used for serializing and deserializing the model.
    """
    
    queryset = Volcanism.objects.all()
    serializer_class = VolcanismSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return CompactedVolcanismSerializer
        return super().get_serializer_class()
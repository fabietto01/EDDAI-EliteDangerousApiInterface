from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter

from ..serializers import StarLuminositySerializer, CompactedStarLuminositySerializer
from ed_body.models import StarLuminosity

class StarLuminosityViewSet(ReadOnlyModelViewSet):
    """
    StarLuminosityViewSet is a viewset for handling CRUD operations on the StarLuminosity model.
    Attributes:
        queryset (QuerySet): A queryset of all StarLuminosity objects.
        serializer_class (type): The serializer class used for serializing and deserializing the model.
    """
    
    queryset = StarLuminosity.objects.all()
    serializer_class = StarLuminositySerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return CompactedStarLuminositySerializer
        return super().get_serializer_class()
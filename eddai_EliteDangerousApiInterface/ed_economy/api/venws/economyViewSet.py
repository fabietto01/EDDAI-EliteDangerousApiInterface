from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter

from ..serializers import EconomySerializer, EconomyBasicInformationSerializer
from ed_economy.models import Economy

class EconomyViewSet(ReadOnlyModelViewSet):
    """
    EconomyViewSet is a viewset for handling CRUD operations on the Economy model.
    Attributes:
        queryset (QuerySet): A queryset of all Economy objects.
        serializer_class (type): The serializer class used for serializing and deserializing the model.
    """
    
    queryset = Economy.objects.all()
    serializer_class = EconomySerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return EconomyBasicInformationSerializer
        return super().get_serializer_class()
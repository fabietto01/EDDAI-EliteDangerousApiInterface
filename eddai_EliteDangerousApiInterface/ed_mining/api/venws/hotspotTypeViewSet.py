from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter

from ..serializers import HotspotTypeModelSerializer

from ed_mining.models import HotspotType

class HotspotTypeViewSet(ReadOnlyModelViewSet):
    """
    HotspotTypeViewSet is a viewset for handling CRUD operations on the HotspotType model.
    Attributes:
        queryset (QuerySet): A queryset of all HotspotType objects.
        serializer_class (type): The serializer class used for serializing and deserializing the model.
    """
    
    queryset = HotspotType.objects.all()
    serializer_class = HotspotTypeModelSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']
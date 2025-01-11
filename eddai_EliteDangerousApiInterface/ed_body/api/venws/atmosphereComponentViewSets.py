from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter

from ..serializers import AtmosphereComponentSerializer, CompactedAtmosphereComponentSerializer

from ed_body.models import AtmosphereComponent

class AtmosphereComponentViewSet(ReadOnlyModelViewSet):
    """
    AtmosphereComponentViewSet is a viewset for handling CRUD operations on the AtmosphereComponent model.
    Attributes:
        queryset (QuerySet): A queryset of all AtmosphereComponent objects.
        filterset_class (type): The
        filter backends (list): A list of filter backends used for filtering and searching.
        search_fields (list): A list of fields that can be searched.
    """
    queryset = AtmosphereComponent.objects.all()
    serializer_class = AtmosphereComponentSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return CompactedAtmosphereComponentSerializer
        return super().get_serializer_class()

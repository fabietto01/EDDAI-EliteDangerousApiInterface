from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter
from django.utils.translation import gettext_lazy as _

from ..serializers import MaterialSerializer, CompactedMaterialSerializer

from ed_material.models import Material

from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(
        description=_("Returns a list of materials with a compact representation.")
    ),
    retrieve=extend_schema(description=_("Returns the details of a material by ID"))
)
class MaterialViewSet(ReadOnlyModelViewSet):
    """
    A viewset for viewing Material instances.
    This ReadOnlyModelViewSet provides read-only access to Material objects.
    It supports searching by the 'name' field and dynamically selects a compacted serializer
    for the 'list' action, while using the default serializer for other actions.
    Attributes:
        queryset (QuerySet): All Material objects.
        serializer_class (Serializer): Default serializer for Material.
        filter_backends (list): List of filter backends, including SearchFilter.
        search_fields (list): Fields to enable search functionality.
    Methods:
        get_serializer_class():
            Returns the serializer class to use for the request.
            Uses CompactedMaterialSerializer for 'list' action,
            otherwise falls back to the default serializer.
    """
    
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return CompactedMaterialSerializer
        return super().get_serializer_class()

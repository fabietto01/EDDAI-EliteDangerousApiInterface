from rest_framework.viewsets import ReadOnlyModelViewSet
from django.utils.translation import gettext_lazy as _

from rest_framework.filters import SearchFilter

from ..serializers import AtmosphereTypeSerializer, CompactedAtmosphereTypeSerializer
from ed_body.models import AtmosphereType

from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    list=extend_schema(
        description=_("Returns a list of atmosphere types with a compact representation.")
    ),
    retrieve=extend_schema(description=_("Returns the details of an atmosphere type by ID"))
)
class AtmosphereTypeViewSet(ReadOnlyModelViewSet):
    """
    A read-only view set for retrieving and searching AtmosphereType objects.
    This view set provides endpoints to list and retrieve atmosphere types, supporting search by name.
    Depending on the action, it uses either the default serializer or a compacted serializer for list actions.
    Attributes:
        queryset (QuerySet): All AtmosphereType objects.
        serializer_class (Serializer): Default serializer for AtmosphereType.
        filter_backends (list): List of filter backends, enabling search functionality.
        search_fields (list): Fields to search on, currently only 'name'.
    Methods:
        get_serializer_class():
            Returns the serializer class to use for the request.
            Uses CompactedAtmosphereTypeSerializer for list actions, otherwise defaults to the superclass implementation.
    """
    
    queryset = AtmosphereType.objects.all()
    serializer_class = AtmosphereTypeSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return CompactedAtmosphereTypeSerializer
        return super().get_serializer_class()

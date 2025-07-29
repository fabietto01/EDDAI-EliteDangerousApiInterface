from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter
from django.utils.translation import gettext_lazy as _

from ..serializers import AtmosphereComponentSerializer, CompactedAtmosphereComponentSerializer

from ed_body.models import AtmosphereComponent

from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(
        description=_("Returns a list of atmosphere components with a compact representation.")
    ),
    retrieve=extend_schema(description=_("Returns the details of an atmosphere component by ID"))
)
class AtmosphereComponentViewSet(ReadOnlyModelViewSet):
    """
    A viewset for viewing AtmosphereComponent instances.
    This ReadOnlyModelViewSet provides read-only access to AtmosphereComponent objects.
    It supports searching by the 'name' field and dynamically selects a compacted serializer
    for the 'list' action, while using the default serializer for other actions.
    Attributes:
        queryset (QuerySet): All AtmosphereComponent objects.
        serializer_class (Serializer): Default serializer for AtmosphereComponent.
        filter_backends (list): List of filter backends, including SearchFilter.
        search_fields (list): Fields to enable search functionality.
    Methods:
        get_serializer_class():
            Returns the serializer class to use for the request.
            Uses CompactedAtmosphereComponentSerializer for 'list' action,
            otherwise falls back to the default serializer.
    """
    
    queryset = AtmosphereComponent.objects.all()
    serializer_class = AtmosphereComponentSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return CompactedAtmosphereComponentSerializer
        return super().get_serializer_class()

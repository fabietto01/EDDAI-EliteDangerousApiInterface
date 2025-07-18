from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter

from ..serializers import StarTypeSerializer, CompactedStarTypeSerializer
from ed_body.models import StarType

from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    list=extend_schema(
        description=_("Returns a list of star types with a compact representation.")
    ),
    retrieve=extend_schema(description=_("Returns the details of a star type by ID"))
)
class StarTypeViewSet(ReadOnlyModelViewSet):
    """
    StarTypeViewSet is a viewset for handling CRUD operations on the StarType model.
    Attributes:
        queryset (QuerySet): A queryset of all StarType objects.
        serializer_class (type): The serializer class used for serializing and deserializing the model.
    """
    
    queryset = StarType.objects.all()
    serializer_class = StarTypeSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return CompactedStarTypeSerializer
        return super().get_serializer_class()
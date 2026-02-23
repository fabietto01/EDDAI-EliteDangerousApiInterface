from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from ..serializers import MaterialSerializer, BaseMaterialSerializer
from ..filterSet import MaterialFilterSet
from ed_material.models import Material

from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes
)

@extend_schema_view(
    list=extend_schema(
        description=_("Retrieve a list of all materials available in the game."),
        parameters=[
            OpenApiParameter(name='grade', description=_("Filter materials by their grade."), required=False, type=OpenApiTypes.INT, enum=Material.MaterialGrade.values, many=True),
            OpenApiParameter(name='type', description=_("Filter materials by their type."), required=False, type=OpenApiTypes.STR, enum=Material.MaterialType.values, many=True),
        ]
    ),
    retrieve=extend_schema(
        description=_("Get detailed information about a specific material by its ID."),
    ),
)
class MaterialViewSet(ReadOnlyModelViewSet):
    """
    MaterialViewSet is a viewset for handling CRUD operations on the Material model.
    Attributes:
        queryset (QuerySet): A queryset of all Material objects.
        serializer_class (type): The serializer class used for serializing and deserializing the model.
    """
    
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer
    filterset_class = MaterialFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return BaseMaterialSerializer
        return super().get_serializer_class()
from core.api.viewsets import OwnerAndDateModelViewSet
from ed_core.api.mixins import DistanceModelMixin

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from ..serializers import StarSerializer, StarDistanceSerializer
from ..filterSet import StarFilterSet

from ed_body.models import Star

from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(
        description="Returns a list of stars, if the parameter distance_by_system is passed,\
            it returns the distance between stars in the distance_st field",
        responses={200: StarDistanceSerializer(many=True)}
    ),
    retrieve=extend_schema(description="Returns the details of a stars by ID")
)
class StarViewSet(DistanceModelMixin, OwnerAndDateModelViewSet):
    """
    StarViewSet is a view set for handling API requests related to the Star model.
    Attributes:
        queryset (QuerySet): A queryset containing all Star objects.
        serializer_class (Serializer): The serializer class used for Star objects.
        filter_backends (list): A list of filter backends used for filtering the queryset.
        search_fields (list): A list of fields that can be searched using the search filter.
    """
    
    queryset = Star.objects.all()
    serializer_class = StarSerializer
    distance_serializer_class = StarDistanceSerializer
    filter_param_distance = 'distance_by_system'
    filterset_class = StarFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
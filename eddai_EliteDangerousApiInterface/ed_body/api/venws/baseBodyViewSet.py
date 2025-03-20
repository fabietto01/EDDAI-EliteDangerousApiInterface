from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from ed_core.api.mixins import DistanceModelMixin

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from ..filterSet import BaseBodyFilterSet
from ..serializers import BaseBodySerializer, BaseBodyDistanceSerializer

from ed_body.models import BaseBody

from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(
        description="Returns a list of base bodies, if the parameter distance_by_system is passed,\
            it returns the distance between base bodies in the distance_st field",
        responses={200: BaseBodyDistanceSerializer(many=True)}
    ),
    retrieve=extend_schema(description="Returns the details of a base bodies by ID"),
)
class BaseBodyViewSet(DistanceModelMixin, ListModelMixin, GenericViewSet):
    """
    BaseBodyViewSet is a view set that provides list and retrieve actions for the BaseBody model.
    Attributes:
        queryset (QuerySet): A queryset that retrieves all BaseBody objects, selecting related 'star' and 'planet' objects.
        serializer_class (Serializer): The serializer class used to serialize and deserialize BaseBody instances.
        filterset_class (FilterSet): The filter set class used to filter the queryset.
        filter_backends (list): A list of filter backends used to filter the queryset.
        search_fields (list): A list of fields that can be searched using the search filter backend.
    """
    
    queryset = BaseBody.objects.all().select_related("star", "planet")
    serializer_class = BaseBodySerializer
    distance_serializer_class = BaseBodyDistanceSerializer
    filter_param_distance = 'distance_by_system'
    filterset_class = BaseBodyFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']

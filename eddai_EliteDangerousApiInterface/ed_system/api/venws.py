from core.api.viewsets import OwnerAndDateModelViewSet
from ed_core.api.mixins import DistanceModelMixin

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import SystemSerializer, SystemDistanceSerializer
from .filters import SystemFilterSet

from ed_system.models import System

class SystemViewSet(DistanceModelMixin, OwnerAndDateModelViewSet):
    """
    SystemViewSet is a viewset for handling CRUD operations on the System model.
    Attributes:
        queryset (QuerySet): A queryset of all System objects.
        filterset_class (type): The filter set class used for filtering the queryset.
        filter_backends (list): A list of filter backends used for filtering and searching.
        search_fields (list): A list of fields that can be searched.
    Methods:
        get_serializer_class(self):
            Returns the appropriate serializer class based on the request query parameters.
            If 'order_by_system' is present in the query parameters, returns SystemDistanceSerializer.
            Otherwise, returns SystemSerializer.
    """
    queryset = System.objects.all()
    serializer_class = SystemSerializer
    distance_serializer_class = SystemDistanceSerializer
    filter_param_distance = 'order_by_system'
    filterset_class = SystemFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
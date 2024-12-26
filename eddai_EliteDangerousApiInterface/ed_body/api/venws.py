from core.api.viewsets import OwnerAndDateModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .serializers import BaseBodySerializer, StarSerializer, PlanetSerializer

from ed_body.models import BaseBody, Star, Planet

class BaseBodyViewSet(OwnerAndDateModelViewSet):
    """
    BaseBodyViewSet is a viewset for handling CRUD operations on the BaseBody model.
    Attributes:
        queryset (QuerySet): A queryset of all BaseBody objects.
        filterset_class (type): The filter set class used for filtering the queryset.
        filter_backends (list): A list of filter backends used for filtering and searching.
        search_fields (list): A list of fields that can be searched.
    Methods:
        get_serializer_class(self):
            Returns the appropriate serializer class based on the request query parameters.
            If 'order_by_system' is present in the query parameters, returns SystemDistanceSerializer.
            Otherwise, returns SystemSerializer.
    """
    queryset = BaseBody.objects.all().select_related("star", "planet")
    filterset_class = None
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']

    def get_serializer_class(self) -> BaseBodySerializer:
        if self.action == 'retrieve':
            if hasattr(self.istance, 'planet'):
                return PlanetSerializer
            if hasattr(self.istance, 'star'):
                return StarSerializer
        return BaseBodySerializer
    
    def get_object(self):
        obj = super().get_object()
        if self.action == 'retrieve':
            self.istance = obj
            if hasattr(obj, 'planet'):
                return obj.planet
            if hasattr(obj, 'star'):
                return obj.star
        return obj
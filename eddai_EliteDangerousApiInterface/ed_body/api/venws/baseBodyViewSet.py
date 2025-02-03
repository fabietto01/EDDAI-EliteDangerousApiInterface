from core.api.viewsets import OwnerAndDateModelViewSet
from django.utils.translation import gettext_lazy as _

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from ..filterSet import BaseBodyFilterSet
from ..serializers import (
    BaseBodySerializer, BaseBodyDistanceSerializer,
    StarSerializer, PlanetSerializer
)

from ed_body.models import BaseBody

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
    filterset_class = BaseBodyFilterSet

    def get_serializer_class(self) -> BaseBodySerializer:
        if self.action == 'retrieve':
            if hasattr(self.instance, 'planet'):
                return PlanetSerializer
            if hasattr(self.instance, 'star'):
                return StarSerializer
        if self.request.query_params.get('order_by_system'):
            return BaseBodyDistanceSerializer
        return BaseBodySerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.query_params.get('order_by_system'):
            return queryset.order_by('name')
        return queryset
    
    def get_object(self):
        obj = super().get_object()
        if self.action == 'retrieve':
            self.instance = obj
            if hasattr(obj, 'planet'):
                return obj.planet
            if hasattr(obj, 'star'):
                return obj.star
        return obj
from core.api.viewsets import OwnerAndDateModelViewSet
from ed_core.api.mixins import DistanceModelMixin

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from ..filterset import RingFilterSet
from ..serializers import RingModelSerializer, RingDistanceSerializer

from ed_mining.models import Ring

class RingViewSet(DistanceModelMixin, OwnerAndDateModelViewSet):
    """
    RingViewSet is a view set for handling API requests related to Ring objects.
    Inherits from:
        OwnerAndDateModelViewSet: A custom view set that includes owner and date information.
    Attributes:
        queryset (QuerySet): A Django QuerySet that retrieves all Ring objects.
        serializer_class (Serializer
    """

    queryset = Ring.objects.all()
    serializer_class = RingModelSerializer
    distance_serializer_class = RingDistanceSerializer
    filter_param_distance = 'distance_by_system'
    filterset_class = RingFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
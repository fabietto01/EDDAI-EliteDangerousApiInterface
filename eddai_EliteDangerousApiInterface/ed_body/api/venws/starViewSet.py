from core.api.viewsets import OwnerAndDateModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from ..serializers import StarSerializer
from ..filterSet import StarFilterSet

from ed_body.models import Star

class StarViewSet(OwnerAndDateModelViewSet):
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
    filterset_class = StarFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
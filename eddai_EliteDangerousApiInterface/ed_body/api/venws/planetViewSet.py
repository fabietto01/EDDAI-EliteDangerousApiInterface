from core.api.viewsets import OwnerAndDateModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from ..serializers import PlanetSerializer
from ..filterSet import PlanetFilterSet

from ed_body.models import Planet

class PlanetViewSet(OwnerAndDateModelViewSet):
    """
    PlanetViewSet is a view set for handling API requests related to Planet objects.
    Inherits from:
        OwnerAndDateModelViewSet: A custom view set that includes owner and date information.
    Attributes:
        queryset (QuerySet): A Django QuerySet that retrieves all Planet objects.
        serializer_class (Serializer): The serializer class used to convert Planet objects to and from JSON.
        filter_backends (list): A list of filter backends used to filter and search the queryset.
        search_fields (list): A list of fields that can be searched using the search filter backend.
    """
    
    queryset = Planet.objects.all()
    serializer_class = PlanetSerializer
    filterset_class = PlanetFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
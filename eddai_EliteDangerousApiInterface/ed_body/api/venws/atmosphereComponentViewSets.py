from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from ..serializers import AtmosphereComponentSerializer

from ed_body.models import AtmosphereComponent

class AtmosphereComponentViewSet(ReadOnlyModelViewSet):
    """
    AtmosphereComponentViewSet is a viewset for handling CRUD operations on the AtmosphereComponent model.
    Attributes:
        queryset (QuerySet): A queryset of all AtmosphereComponent objects.
        filterset_class (type): The
        filter backends (list): A list of filter backends used for filtering and searching.
        search_fields (list): A list of fields that can be searched.
    """
    queryset = AtmosphereComponent.objects.all()
    filterset_class = None
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
    
    serializer_class = AtmosphereComponentSerializer

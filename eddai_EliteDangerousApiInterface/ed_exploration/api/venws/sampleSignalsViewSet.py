from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter
from django.utils.translation import gettext_lazy as _

from ..serializers import SampleSignalsSerializer

from ed_exploration.models import SampleSignals

from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(description=_("Returns a list of all sample types.")),
    retrieve=extend_schema(description=_("Returns the details of a sample type by ID."))
)
class SampleSignalsViewSet(ReadOnlyModelViewSet):
    """
    SampleSignalsViewSet is a viewset for handling read-only operations on the SampleSignals model.
    Attributes:
        queryset (QuerySet): A queryset of all SampleSignals objects.
        serializer_class (type): The serializer class used for serializing and deserializing the model.
    """
    
    queryset = SampleSignals.objects.all()
    serializer_class = SampleSignalsSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

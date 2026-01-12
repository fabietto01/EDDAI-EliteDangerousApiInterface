from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter
from django.utils.translation import gettext_lazy as _

from ..serializers import SignalSignalsSerializer

from ed_exploration.models import SignalSignals

from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(description=_("Returns a list of all signal types.")),
    retrieve=extend_schema(description=_("Returns the details of a signal type by ID."))
)
class SignalSignalsViewSet(ReadOnlyModelViewSet):
    """
    SignalSignalsViewSet is a viewset for handling read-only operations on the SignalSignals model.
    Attributes:
        queryset (QuerySet): A queryset of all SignalSignals objects.
        serializer_class (type): The serializer class used for serializing and deserializing the model.
    """
    
    queryset = SignalSignals.objects.all()
    serializer_class = SignalSignalsSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

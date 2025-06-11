from rest_framework.viewsets import ReadOnlyModelViewSet
from django.utils.translation import gettext_lazy as _

from rest_framework.filters import SearchFilter

from ..serializers import StationTypeSerializer, StationTypeBasicInformationSerializer
from ed_station.models import StationType

from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(
        description=_("Returns a list of station types with basic information.")
    ),
    retrieve=extend_schema(description=_("Returns the details of a station type by ID"))
)
class StationTypeViewSet(ReadOnlyModelViewSet):    
    queryset = StationType.objects.all()
    serializer_class = StationTypeSerializer
    filter_backends = [SearchFilter,]
    search_fields = ['name']

    def get_serializer_class(self):
        """
        Returns the serializer class based on the action.
        If the action is 'list', it returns the StationTypeSerializer.
        Otherwise, it returns the default serializer class.
        """
        if self.action == 'list':
            return StationTypeBasicInformationSerializer
        return super().get_serializer_class()
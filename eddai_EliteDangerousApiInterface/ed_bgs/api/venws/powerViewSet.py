from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter
from ed_bgs.api.serializers import PowerSerializer, PowerBasicInformationSerializer
from ed_bgs.models import Power
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(description=_("Retrieve a list of all powers available in the game.")),
    retrieve=extend_schema(description=_("Get detailed information about a specific power by its ID.")),
)
class PowerViewSet(ReadOnlyModelViewSet):
    queryset = Power.objects.select_related('headquarter', 'allegiance')
    serializer_class = PowerSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return PowerBasicInformationSerializer
        return super().get_serializer_class()

from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from ed_bgs.api.filterSet.powerStateFilterSet import PowerStateFilterSet
from ed_bgs.api.serializers import PowerStateSerializer, PowerStateBasicInformationSerializer
from ed_bgs.models import PowerState
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(description=_("Retrieve a list of all power states available in the game.")),
    retrieve=extend_schema(description=_("Get detailed information about a specific power state by its ID.")),
)
class PowerStateViewSet(ReadOnlyModelViewSet):
    queryset = PowerState.objects.all()
    serializer_class = PowerStateSerializer
    filterset_class = PowerStateFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return PowerStateBasicInformationSerializer
        return super().get_serializer_class()

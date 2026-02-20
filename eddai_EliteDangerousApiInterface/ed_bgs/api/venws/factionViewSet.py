from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter
from ed_bgs.api.serializers import FactionSerializer, FactionBasicInformationSerializer
from ed_bgs.models import Faction
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(description=_("Retrieve a list of all factions available in the game.")),
    retrieve=extend_schema(description=_("Get detailed information about a specific faction by its ID.")),
)
class FactionViewSet(ReadOnlyModelViewSet):
    queryset = Faction.objects.all()
    serializer_class = FactionSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return FactionBasicInformationSerializer
        return super().get_serializer_class()

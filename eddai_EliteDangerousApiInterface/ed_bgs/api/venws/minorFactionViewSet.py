from rest_framework.filters import SearchFilter
from core.api.viewsets import OwnerAndDateModelViewSet
from ed_bgs.api.serializers import MinorFactionSerializer, MinorFactionBasicInformation
from ed_bgs.models import MinorFaction
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(description=_("Retrieve a list of all minor factions.")),
    retrieve=extend_schema(description=_("Get detailed information about a specific minor faction by its ID.")),
    create=extend_schema(description=_("Create a new minor faction.")),
    update=extend_schema(description=_("Update an existing minor faction.")),
    destroy=extend_schema(description=_("Delete a minor faction.")),
)
class MinorFactionViewSet(OwnerAndDateModelViewSet):
    queryset = MinorFaction.objects.select_related('allegiance', 'government', 'created_by', 'updated_by')
    serializer_class = MinorFactionSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return MinorFactionBasicInformation
        return super().get_serializer_class()

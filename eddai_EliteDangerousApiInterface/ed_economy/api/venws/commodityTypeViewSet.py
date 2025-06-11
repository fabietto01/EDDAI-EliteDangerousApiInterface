from rest_framework.viewsets import ReadOnlyModelViewSet

from rest_framework.filters import SearchFilter

from ..serializers import CommoditySerializer, CompactedCommoditySerializer
from ed_economy.models import Commodity

from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, extend_schema_view


@extend_schema_view(
    list=extend_schema(
        description=_("Retrieve a list of all commodities available in the game."),
    ),
    retrieve=extend_schema(
        description=_("Get detailed information about a specific commodity by its ID."),
    ),
)
class CommodityViewSet(ReadOnlyModelViewSet):

    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return CompactedCommoditySerializer
        return super().get_serializer_class()
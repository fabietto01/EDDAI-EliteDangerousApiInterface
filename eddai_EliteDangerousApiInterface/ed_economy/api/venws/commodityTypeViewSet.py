from rest_framework.viewsets import ReadOnlyModelViewSet

from rest_framework.filters import SearchFilter

from ..serializers import CommoditySerializer, CompactedCommoditySerializer
from ed_economy.models import Commodity

class CommodityViewSet(ReadOnlyModelViewSet):

    queryset = Commodity.objects.all()
    serializer_class = CommoditySerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return CompactedCommoditySerializer
        return super().get_serializer_class()
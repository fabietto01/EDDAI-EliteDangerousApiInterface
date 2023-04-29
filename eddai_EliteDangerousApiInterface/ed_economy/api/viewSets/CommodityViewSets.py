from rest_framework import viewsets
from core.api.permissions import IsAdminUserOrReadOnly

from ed_economy.api.serializers import CommodityModelSerializes

from ed_economy.models import Commodity

class CommodityViewSet(viewsets.ModelViewSet):

    queryset = Commodity.objects.all()
    serializer_class = CommodityModelSerializes
    filterset_fields = ['name']
    permission_classes = [IsAdminUserOrReadOnly]


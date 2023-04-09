from rest_framework import serializers
from eddn.service.seriallizers.BaseSerializer import BaseSerializer
from eddn.service.commodity.CommoditySerializer import CommoditySerializer

from core.utility import update_or_create_if_time

class CommodityV3Serializer(BaseSerializer):
    """
    serializer dedicato alla lavorazione dei dati con scema commodityV3
    link dello scemma https://eddn.edcd.io/schemas/commodity-v3.0.json
    """
    systemName = serializers.CharField(
        min_length=1
    )
    stationName = serializers.CharField(
        min_length=1
    )
    commodities = serializers.ListField(
        child=CommoditySerializer(),
        min_length=1
    )
    timestamp = serializers.DateTimeField(
        input_formats=[
            "%Y-%m-%dT%H:%M:%SZ"
        ]
    )

    def update_or_create(self, validated_data: dict):
        return super().update_or_create(validated_data)

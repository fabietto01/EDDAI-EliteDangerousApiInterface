from rest_framework import serializers
from eddn.service.seriallizers.BaseSerializer import BaseSerializer
from eddn.service.commodity.CommoditySerializer import CommoditySerializer

from ed_system.models import System
from ed_station.models import Station

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
    economies  = None
    StationType = None
    timestamp = serializers.DateTimeField(
        input_formats=[
            "%Y-%m-%dT%H:%M:%SZ"
        ]
    )

    def set_data_defaults(self, validated_data: dict) -> dict:
        return {}
    
    def data_preparation(self, validated_data: dict) -> dict:
        self.commodities_data:dict = validated_data.pop('commodities', None)

    def create_dipendent(self, instance):
        pass

    def update_dipendent(self, instance):
        pass

    def update_or_create(self, validated_data: dict):
        self.data_preparation(validated_data)
        system = System.objects.get(name=validated_data.get('systemName'))
        self.instance, create = update_or_create_if_time(
            Station, time=self.get_time(), defaults=self.get_data_defaults(validated_data),
            update_function=self.update_dipendent, create_function=self.create_dipendent,
            name=validated_data.get('stationName'), system=system
        )
        return self.instance
from rest_framework import serializers
from eddn.service.seriallizers.BaseSerializer import BaseSerializer
from eddn.service.seriallizers.commodity.CommoditySerializer import CommoditySerializer
from eddn.service.seriallizers.commodity.EconomieSerializer import EconomieSerializer

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
    economies  = serializers.ListField(
        child=EconomieSerializer(),
        min_length=1,
        required=False
    )
    StationType = None
    timestamp = serializers.DateTimeField(
        input_formats=[
            "%Y-%m-%dT%H:%M:%SZ"
        ]
    )

    def validate_systemName(self, value:str):
        """
        controlla che il sistema esista nel database
        """
        if not System.objects.filter(name=value).exists():
            raise serializers.ValidationError('System not found')
        return value

    def set_data_defaults(self, validated_data: dict) -> dict:
        economies = sorted(
            validated_data.get('economies', [{}]),
            key=lambda economy: economy.get('proportion', 0),
        )
        return {
            'primaryEconomy': economies[0].get('name', None),
            'secondaryEconomy': economies[1].get('name', None),
        }
    
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
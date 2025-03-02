from ..baseSerializer import BaseSerializer
from rest_framework import serializers

from ..nestedSerializers import EconomyLowerSerializer, CommoditySerializer

from ed_system.models import System
from ed_economy.models import Economy
from ed_station.models import Station

from core.utility import create_or_update_if_time, in_list_models

class CommodityV3Serializer(BaseSerializer):
    systemName = serializers.CharField(
        min_length=1
    )
    marketId = serializers.IntegerField(
        min_value=0,
    )
    stationName = serializers.CharField(
        min_length=1
    )
    economies = EconomyLowerSerializer(
        many=True, required=False
    )
    commodities = CommoditySerializer(
        many=True
    )
    timestamp = serializers.DateTimeField(
        input_formats=[
            "%Y-%m-%dT%H:%M:%SZ"
        ],
        source="updated_at"
    )

    def _sort_economies(self, StationEconomies:list[dict]) -> None:
        """Sort the station economies by their proportion in descending order."""
        StationEconomies.sort(key=lambda x: x.get('proportion'), reverse=True)

    def _get_primary_economy(self, data) -> Economy:
        """Get the primary economy from the sorted list of station economies."""
        StationEconomies:list[dict] = data.get('economies', [])
        if not StationEconomies:
            return None
        self._sort_economies(StationEconomies)
        return StationEconomies[0].get('name')
    
    def _get_secondary_economy(self, data) -> Economy:
        """Get the secondary economy from the sorted list of station economies."""
        StationEconomies:list[dict] = data.get('economies', [])
        if not StationEconomies:
            return None
        if len(StationEconomies) == 1:
            return Economy.objects.get(eddn='$economy_None;')
        self._sort_economies(StationEconomies)
        return StationEconomies[1].get('name')

    def validate(self, attrs):
        if not System.objects.filter(name=attrs.get('systemName')).exists():
            raise serializers.ValidationError('System not found')
        return super().validate(attrs)
    
    def set_data_defaults(self, validated_data):
        return {
            "name": validated_data.get('StationName'),
            "system":validated_data.get('system'),
            "primaryEconomy": self._get_primary_economy(validated_data),
            "secondaryEconomy": self._get_secondary_economy(validated_data),
        }
    
    def set_data_defaults_create(self, validated_data):
        return {
            "created_by": validated_data.get('created_by'),
            "updated_by": validated_data.get('updated_by'),
            "updated_at": validated_data.get('updated_at'),
            "created_at": validated_data.get('updated_at'),
        }

    def set_data_defaults_update(self, validated_data):
        return {
            "updated_by": validated_data.get('updated_by'),
            "updated_at": validated_data.get('updated_at'),
        }

    def run_update_commodities(self, instance, validated_data):
        serializer = CommoditySerializer(
            data=self.initial_data.get('commodities', []), many=True,
            context={'station': instance}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(
            created_by=validated_data.get('created_by'),
            updated_by=validated_data.get('updated_by'),
            updated_at=validated_data.get('updated_at'),
            station=instance
        )
    
    def create_dipendent(self, instance, validated_data):
        self.run_update_commodities(instance, validated_data)

    def update_dipendent(self, instance, validated_data):
        self.run_update_commodities(instance, validated_data)

    def update_or_create(self, validated_data):
        def_create_dipendent = lambda instance: self.create_dipendent(instance, validated_data)
        def_update_dipendent = lambda instance: self.update_dipendent(instance, validated_data)
        system = System.objects.get(name=validated_data.get('systemName'))
        station, create = create_or_update_if_time(
            Station, time=self.get_time(),
            defaults=self.get_data_defaults(validated_data, system=system),
            defaults_update=self.get_data_defaults_update(validated_data),
            defaults_create=self.get_data_defaults_create(validated_data),
            update_function=def_update_dipendent,
            create_function=def_create_dipendent,
            markerid=validated_data.get('marketId'),
        )
        return station
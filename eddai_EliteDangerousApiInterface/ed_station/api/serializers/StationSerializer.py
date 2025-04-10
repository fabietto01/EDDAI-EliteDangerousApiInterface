from rest_framework import serializers

from ed_core.api.serializers.DistanceSerializer import DistanceSerializer

from .stationTypeBasicInformationSerializer import StationTypeBasicInformationSerializer
from ed_system.api.serializers import SystemBasicInformation
from ed_economy.api.serializers import EconomyBasicInformationSerializer, CommodityInStatioBasicInformation
from ed_bgs.api.serializers import MinorFactionBasicInformation

from ed_station.models import Station, StationType, Service
from ed_economy.models import Economy
from ed_system.models import System

class StationBasicInformation(serializers.ModelSerializer):
    
    class Meta:
        model = Station
        fields = ['id', 'name']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
        }

class StationSerializer(StationBasicInformation):
    
    system = SystemBasicInformation(
        read_only=True,
    )
    system_id = serializers.PrimaryKeyRelatedField(
        queryset=System.objects.all(),
        source='system',
        write_only=True,
    )

    type = StationTypeBasicInformationSerializer(
        read_only=True,
    )
    type_id = serializers.PrimaryKeyRelatedField(
        queryset=StationType.objects.all(),
        source='type',
        write_only=True,
    )

    primaryEconomy = EconomyBasicInformationSerializer(
        read_only=True,
    )
    primaryEconomy_id = serializers.PrimaryKeyRelatedField(
        queryset=Economy.objects.all(),
        source='primaryEconomy',
        write_only=True,
    )

    secondaryEconomy = EconomyBasicInformationSerializer(
        read_only=True,
    )
    secondaryEconomy_id = serializers.PrimaryKeyRelatedField(
        queryset=Economy.objects.all(),
        source='secondaryEconomy',
        write_only=True,
    )

    minorFaction = MinorFactionBasicInformation(
        read_only=True,
    )
    minorFaction_id = serializers.PrimaryKeyRelatedField(
        queryset=Station.objects.all(),
        source='minorFaction',
        write_only=True,
    )

    service = serializers.SlugRelatedField(
        slug_field='name',
        many=True,
        read_only=True,
    )
    service_id = serializers.PrimaryKeyRelatedField(
        queryset=Service.objects.all(),
        source='service',
        write_only=True,
        many=True,
    )

    class Meta(StationBasicInformation.Meta):
        fields = None
        exclude = ['commodity']

class StationDistanceSerializer(StationSerializer, DistanceSerializer):
    
    class Meta(StationSerializer.Meta):
        pass
from rest_framework import serializers
from .baseJournalSerializer import BaseJournalSerializer

from ..customFields import LandingPadsChoiceField
from ..nestedSerializers import EconomySerializer, MinorFactionSerializer

from ed_station.models import (
    Service, StationType,
    Station
)
from ed_bgs.models import MinorFaction, MinorFactionInSystem


class DockedSerializer(BaseJournalSerializer):
    LandingPads = LandingPadsChoiceField(
        choices=[key for key in Station.LandingPadChoices.names],
    )
    StationName = serializers.CharField(
        min_length=1,
    )
    StationType = serializers.SlugRelatedField(
        queryset=StationType.objects.all(),
        slug_field='eddn',
    )
    DistFromStarLS = serializers.FloatField(
        min_value=0,
    )
    StationServices = serializers.SlugRelatedField(
        queryset=Service.objects.all(),
        slug_field='eddn',
        many=True,
    )
    StationEconomies = serializers.ListField(
        child=EconomySerializer(),
        min_length = 1,
        max_length = 2,
    )
    StationFaction = MinorFactionSerializer()

    def validate(self, attrs:dict):
        economies = attrs.get('StationEconomies', [])
        faction_Name = attrs.get('StationFaction', {}).get('Name')
        system_Name = attrs.get('StarSystem')
        if len(economies) == 2:
            if economies[0].get('Name', '') == economies[1].get('Name', ''):
                raise serializers.ValidationError({'StationEconomies': 'Economies must be different'})
        if not ( attrs.get('StationType', '') == 'FleetCarrier' and faction_Name == 'FleetCarrier' ):
            if not MinorFactionInSystem.objects.filter(system__name=system_Name, minorFaction__name=faction_Name).exists():
                raise serializers.ValidationError({'StationFaction':{'Name':f'the minor faction {faction_Name} is not present in the system {system_Name}'}})
        return super().validate(attrs)
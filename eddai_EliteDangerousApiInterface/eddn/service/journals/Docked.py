from rest_framework import serializers
from eddn.service.journals.BaseJournal import BaseJournal
from eddn.service.seriallizers.customFields.CustomChoiceField import CustomChoiceField, LandingPadsChoiceField

from ed_station.models import (
    Service, ServiceInStation, StationType,
    Station
)
from ed_economy.models import Economy
from core.utility import (
    update_or_create_if_time, in_list_models, 
    get_values_list_or_default, get_or_none
)
from django.db import OperationalError, ProgrammingError

class StationEconomiesSerializer(serializers.Serializer):
    Name = CustomChoiceField(
        choices=get_values_list_or_default(Economy, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
    )

class DockedSerializer(BaseJournal):
    LandingPads = LandingPadsChoiceField(
        choices=[key for key in Station.LandingPadChoices.names],
    )
    StationName = serializers.CharField(
        min_length=1,
    )
    StationType = CustomChoiceField(
        choices=get_values_list_or_default(StationType, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
    )
    DistFromStarLS = serializers.FloatField(
        min_value=0,
    )
    StationServices = serializers.ListField(
        child=CustomChoiceField(
            choices=get_values_list_or_default(Service, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
        )
    )
    StationEconomies = serializers.ListField(
        child=StationEconomiesSerializer(),
        min_length = 1,
        max_length = 2,
    )
    StationFaction = None

    def set_data_defaults(self, validated_data: dict) -> dict:
        return{
            'landingPad': validated_data.get('LandingPads'),
            'type': get_or_none(StationType, eddn=validated_data.get('StationType')),
            'distance': validated_data.get('DistFromStarLS'),

        }

    def update_or_create(self, validated_data: dict):
        sytsem = super().update_or_create(validated_data)
        station, created = update_or_create_if_time(
            Station, time=self.get_time(), 
            defaults=self.get_data_defaults(validated_data),
            system=sytsem, name=validated_data.get('StationName'),
        )
    class Meta:
        model = Station

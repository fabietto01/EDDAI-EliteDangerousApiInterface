from rest_framework import serializers
from eddn.service.seriallizers.BaseSerializer import BaseSerializer
from eddn.service.seriallizers.customFields.CustomChoiceField import HappinessChoiceField

from ed_bgs.models import (
    Faction, Government, MinorFaction, 
    MinorFactionInSystem, State,
)

from core.utility import update_or_create_if_time

class MinorFactionInSystemSerializer(BaseSerializer):
    Name = serializers.CharField(
        min_length=1
    )
    Allegiance = serializers.ChoiceField(
        choices=Faction().get_data_list(),
    )
    Government = serializers.ChoiceField(
        choices=Government().get_data_list(),
    )
    Influence = serializers.FloatField(
        min_value=0, max_value=1,
    )
    Happiness = HappinessChoiceField(
        choices=State().get_data_list(State.TypeChoices.HAPPINESS.value),
    )
    RecoveringStates = None
    ActiveStates = None
    PendingStates = None

    def set_data_defaults_minorFaction(self, validated_data: dict) -> dict:
        return {
            "allegiance": Faction().get_instanze_from_eddn(validated_data.get('Allegiance')),
            "government": Government().get_instanze_from_eddn(validated_data.get('Government')),
        }
    
    def set_data_defaults_MinorFactionInSystem(self, validated_data: dict) -> dict:
        return {
            "Influence": validated_data.get('Influence'),
        }

    def get_data_defaults(self, validated_data:dict, minorFaction:bool=None, MinorFactionInSystem:bool=None) -> dict:
        """
        chiama questo medodo per restituire i default data
        """
        default_data = {}
        if minorFaction:
            default_data = self.set_data_defaults_minorFaction(validated_data)
        if MinorFactionInSystem:
            default_data = self.set_data_defaults_MinorFactionInSystem(validated_data)
        default_data = self.clean_data_defaults(default_data)
        return default_data

    def data_preparation(self, validated_data: dict) -> dict:
        self.happiness = validated_data.get('Happiness', None)

    def create_dipendent(self, instance):
        pass

    def update_dipendent(self, instance):
        pass

    def update_or_create(self, validated_data: dict):
        minorFaction, create = update_or_create_if_time(
            MinorFaction, time=self.get_time(), 
            defaults=self.get_data_defaults(validated_data, minorFaction=True),
            name=validated_data.get('Name'),
        )
        self.data_preparation(validated_data)
        self.instance, create = update_or_create_if_time(
            MinorFactionInSystem, time=self.get_time(), 
            defaults=self.get_data_defaults(validated_data, MinorFactionInSystem=True),
            create_function=self.create_dipendent, update_function=self.update_dipendent,
            system=validated_data.get('system'), minorFaction=minorFaction,
        )
        return self.instance
    

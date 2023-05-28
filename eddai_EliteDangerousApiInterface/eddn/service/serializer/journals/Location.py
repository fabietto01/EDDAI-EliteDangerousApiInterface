from rest_framework import serializers
from .BaseJournal import BaseJournal
from django.db import OperationalError, ProgrammingError
import importlib

from ..customFields import CustomChoiceField
from ..nestedSerializer import MinorFactionInSystemSerializer, BaseMinorFactionSerializer

from ed_station.models import (
    StationType, Station
)

from ed_body.models import Planet, Star
from ed_economy.models import Economy
from ed_system.models import System
from ed_bgs.models import MinorFactionInSystem, MinorFaction, PowerInSystem, Power, PowerState

from core.utility import (
    get_values_list_or_default,
    get_or_none, update_or_create_if_time
)

class LocationSerializer(BaseJournal):
    """
    https://elite-journal.readthedocs.io/en/latest/Travel/#location
    """
    Body = serializers.CharField(
        max_length=255,
    )
    BodyID = serializers.IntegerField(
        min_value=0,
    )
    BodyType = serializers.ChoiceField(
        choices=[
            "Planet", "Star"
        ]
    )

    DistFromStarLS = serializers.FloatField(
        min_value=0,
        required=False,
    )
    #-------------------------------------------------------------------------------
    Docked = serializers.BooleanField()
    StationName = serializers.CharField(
        min_length=1,
        required=False,
    )
    StationType = serializers.ChoiceField(
        choices=get_values_list_or_default(StationType, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
        required=False,
    )
    #-------------------------------------------------------------------------------
    Population = serializers.IntegerField(
        min_value=0,
    )
    SystemEconomy = CustomChoiceField(
        choices=get_values_list_or_default(Economy, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
    )
    SystemSecondEconomy = CustomChoiceField(
        choices=get_values_list_or_default(Economy, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
        required=False,
        allow_blank=True,
    )
    SystemSecurity = CustomChoiceField(
        choices=[sc.lower() for sc in System.SecurityChoices.names],
    )
    SystemFaction = BaseMinorFactionSerializer(
        required=False,
    )
    Factions = serializers.ListField(
        child=MinorFactionInSystemSerializer(),
        required=False,
        min_length=0,
        max_length=MinorFactionInSystem.MaxRelation,
    )
    Conflicts = None
    Powers = serializers.ListField(
        child=serializers.ChoiceField(
            choices=get_values_list_or_default(Power, [], (OperationalError, ProgrammingError), 'name', flat=True),
        ),
        required=False,
        min_length=0,
        max_length=PowerInSystem.MaxRelation,
    )
    PowerplayState = serializers.ChoiceField(
        choices=get_values_list_or_default(PowerState, [], (OperationalError, ProgrammingError), 'eddn', 'name'),
        required=False,
    )

    def validate(self, attrs:dict):
        """
        controlla se Docked è True e in tal caso controlla che StationName e StationType siano presenti
        """ 
        if attrs.get('Docked', False):
            if not attrs.get('StationName', None):
                raise serializers.ValidationError({'StationName': 'This field is required when Docked is True'})
            if not attrs.get('StationType', None):
                raise serializers.ValidationError({'StationType': 'This field is required when Docked is True'})
        if attrs.get('BodyType', None) == "Planet" and not attrs.get('DistFromStarLS', None):
            raise serializers.ValidationError({'DistFromStarLS': 'This field is required when BodyType is Planet'})
        return super().validate(attrs)
    
    def set_data_defaults(self, validated_data: dict) -> dict:
        defaults = BaseJournal.set_data_defaults(self, validated_data)
        defaults.update(
            {
                "primaryEconomy": get_or_none(Economy, eddn=validated_data.get('SystemEconomy', None)),
                "secondaryEconomy": get_or_none(Economy, eddn=validated_data.get('SystemSecondEconomy', None)),
                "security":  System.SecurityChoices[
                    validated_data.get('SystemSecurity', '').capitalize()
                ].value if validated_data.get('SystemSecurity', None) else None,
                "population": validated_data.get('Population', None),
            }
        )
        return defaults
    
    def set_data_defaults_body(self, validated_data: dict) -> dict:
        return {
            'distance': validated_data.get('DistFromStarLS', None),
        }
    
    def set_data_defaults_stastion(self, validated_data: dict) -> dict:
        return {
            'type': get_or_none(StationType, eddn=validated_data.get('StationType', None)),
        }

    def check_control_faction(self, instance:System):
        """
        controlla se la fazione che controlla il sistema corisposnde nel casso la aggiorna
        """
        if self.control_faction:
            minorfaction = MinorFaction.objects.get(name=self.control_faction.get('Name'))
            if not instance.conrollingFaction == minorfaction:
                instance.conrollingFaction = minorfaction
                instance.save(force_update=['conrollingFaction'])

    def update_minor_faction(self, instance):
        for faction in self.factions_data:
            serializer = MinorFactionInSystemSerializer(data=faction)
            if serializer.is_valid():
                serializer.save(
                    system=instance, timestamp=self.get_time()
                )
    
    def create_power(self, instance:PowerState):
        power = self.powers_data.get('Powers', [])
        for p in power:
            instance.powers.add(Power.objects.get(name=p))

    def update_power(self, instance):
        powerqsList = list(instance.powers.all())
        powerList = [Power.objects.get(name=p) for p in self.powers_data.get('Powers', [])]
        for power in powerqsList:
            if not power in powerList:
                instance.powers.remove(power)
        for power in powerList:
            if not power in powerqsList:
                instance.powers.add(power)

    def update_PowerInSystem(self, instance):
        if self.powers_data.get('Powers', []) and self.powers_data.get('PowerplayState', None):
            defaults = {
                'state': PowerState.objects.get(eddn=self.powers_data.get('PowerplayState', None)),
            }
            powerInstanceqs, create = update_or_create_if_time(
                PowerInSystem, time=self.get_time(), defaults=defaults,
                update_function=self.update_power, create_function=self.create_power, 
                system=instance
            )

    def data_preparation(self, validated_data: dict) -> dict:
        self.factions_data:dict = validated_data.pop("Factions", [])
        self.control_faction:dict = validated_data.pop("SystemFaction", None)
        self.powers_data:dict = {
            'Powers': validated_data.pop("Powers", []),
            'PowerplayState': validated_data.pop("PowerplayState", None),
        }

    def create_dipendent(self, instance):
        self.update_minor_faction(instance)
        self.check_control_faction(instance)
        self.update_PowerInSystem(instance)

    def update_dipendent(self, instance):
        self.update_minor_faction(instance)
        self.check_control_faction(instance)
        self.update_PowerInSystem(instance)

    def update_or_create(self, validated_data: dict) -> System:
        self.data_preparation(validated_data)
        systemInstance, systemcreate = update_or_create_if_time(
            System, time=self.get_time(), defaults=self.get_data_defaults(validated_data),
            update_function=self.update_dipendent, create_function=self.create_dipendent,
            name=validated_data.get('StarSystem'),
        )
        __class = eval(validated_data.get('BodyType'))
        bodyInstance, bodycreate = update_or_create_if_time(
            __class, defaults=self.get_data_defaults(validated_data, self.set_data_defaults_body),
            time=self.get_time(),
            system=systemInstance, name=validated_data.get('Body'), bodyID=validated_data.get('BodyID'), 
        )
        if validated_data.get('Docked', False):
            stationInstance, stationcreate = update_or_create_if_time(
                Station, defaults=self.get_data_defaults(validated_data, self.set_data_defaults_stastion),
                time=self.get_time(),
                system=systemInstance, name=validated_data.get('StationName') 
            )
        return systemInstance
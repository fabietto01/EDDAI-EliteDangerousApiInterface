from rest_framework import serializers
from .BaseJournal import BaseJournal
from django.db import OperationalError, ProgrammingError
import uuid

from ..customFields import CustomChoiceField, CustomCacheChoiceField
from ..nestedSerializer import MinorFactionInSystemSerializer, BaseMinorFactionSerializer

from core.api.fields import CacheChoiceField

from ed_station.models import (
    StationType, Station
)

from ed_economy.models import Economy
from ed_system.models import System
from ed_bgs.models import MinorFactionInSystem, MinorFaction, PowerInSystem, Power, PowerState

from core.utility import (
    get_values_list_or_default,
    get_or_none, create_or_update_if_time, in_list_models
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
    StationType = CacheChoiceField(
        fun_choices=lambda:get_values_list_or_default(StationType, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
        cache_key=StationType.get_cache_key(),
        required=False,
    )
    #-------------------------------------------------------------------------------
    Population = serializers.IntegerField(
        min_value=0,
    )
    SystemEconomy = CustomCacheChoiceField(
        fun_choices=lambda: get_values_list_or_default(Economy, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
        cache_key=Economy.get_cache_key(),
    )
    SystemSecondEconomy = CustomCacheChoiceField(
        fun_choices=lambda: get_values_list_or_default(Economy, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
        cache_key=Economy.get_cache_key(),
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
        max_length=MinorFactionInSystem.MaxRelation(),
    )
    Conflicts = None
    Powers = serializers.ListField(
        child=CacheChoiceField(
            fun_choices=lambda: get_values_list_or_default(Power, [], (OperationalError, ProgrammingError), 'name', flat=True),
            cache_key=Power.get_cache_key(),
        ),
        required=False,
        min_length=0,
        max_length=PowerInSystem.MaxRelation(),
    )
    PowerplayState = CacheChoiceField(
        fun_choices=lambda: get_values_list_or_default(PowerState, [], (OperationalError, ProgrammingError), 'eddn', 'name'),
        cache_key=PowerState.get_cache_key(),
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
        defaults = super().set_data_defaults(validated_data)
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
                instance.updated_by = self.agent
                instance.save(force_update=['conrollingFaction'])

    def update_minor_faction(self, instance):
        for faction in self.factions_data:
            serializer = MinorFactionInSystemSerializer(data=faction)
            if serializer.is_valid():
                serializer.save(
                    system=instance, timestamp=self.get_time()
                )
    
    def create_PowerInSystem(self, instance:System):
        Powers = self.powers_data.get('Powers', [])
        PowerplayState = self.powers_data.get('PowerplayState', None)
        if Powers and PowerplayState:
            serviceList = [
                PowerInSystem(
                    system=instance, 
                    power=Power.objects.get(name=power), 
                    state=PowerState.objects.get(eddn=PowerplayState),
                    created_by=self.agent, updated_by=self.agent
                ) for power in Powers
            ]
            PowerInSystem.objects.bulk_create(serviceList)

    def update_PowerInSystem(self, instance:System):
        Powers = self.powers_data.get('Powers', [])
        PowerplayState = self.powers_data.get('PowerplayState', None)
        if Powers and PowerplayState:
            powerinsystem_create:list[PowerInSystem] = []
            powerinsystem_delete:list[PowerInSystem] = []
            powerinsystemqs = PowerInSystem.objects.filter(system=instance)
            powerinsystemList = [
                PowerInSystem(
                    system=instance, 
                    power=Power.objects.get(name=power), 
                    state=PowerState.objects.get(eddn=PowerplayState),
                    created_by=self.agent, updated_by=self.agent
                ) for power in Powers
            ]
            for power in powerinsystemList:
                if not in_list_models(power, powerinsystemqs):
                    powerinsystem_create.append(power)
            for power in powerinsystemqs:
                if not in_list_models(power, powerinsystemList):
                    powerinsystem_delete.append(power.id)
            if powerinsystem_create:
                PowerInSystem.objects.bulk_create(powerinsystem_create)
            if powerinsystem_delete:
                PowerInSystem.objects.filter(id__in=powerinsystem_delete).delete()

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
        systemInstance, systemcreate = create_or_update_if_time(
            System, time=self.get_time(), defaults=self.get_data_defaults(validated_data),
            defaults_create=self.get_data_defaults_create(), defaults_update=self.get_data_defaults_update(),
            update_function=self.update_dipendent, create_function=self.create_dipendent,
            name=validated_data.get('StarSystem'),
        )
        __class = eval(validated_data.get('BodyType'))
        bodyInstance, bodycreate = create_or_update_if_time(
            __class, defaults=self.get_data_defaults(validated_data, self.set_data_defaults_body),
            defaults_create=self.get_data_defaults_create(), defaults_update=self.get_data_defaults_update(),
            time=self.get_time(),
            system=systemInstance, name=validated_data.get('Body'), bodyID=validated_data.get('BodyID'), 
        )
        if validated_data.get('Docked', False):
            stationInstance, stationcreate = create_or_update_if_time(
                Station, defaults=self.get_data_defaults(validated_data, self.set_data_defaults_stastion),
                defaults_create=self.get_data_defaults_create(), defaults_update=self.get_data_defaults_update(),
                time=self.get_time(),
                system=systemInstance, name=validated_data.get('StationName') 
            )
        return systemInstance
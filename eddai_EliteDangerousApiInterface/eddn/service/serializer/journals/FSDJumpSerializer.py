from rest_framework import serializers
from django.db import OperationalError, ProgrammingError
import uuid

from .BaseJournal import BaseJournal

from ..customFields import CustomChoiceField, CustomCacheChoiceField
from ..nestedSerializer import MinorFactionInSystemSerializer, BaseMinorFactionSerializer

from ed_system.models import System
from ed_economy.models import Economy
from ed_bgs.models import MinorFactionInSystem, MinorFaction, PowerInSystem, Power, PowerState

from core.utility import create_or_update_if_time, get_values_list_or_default, get_or_none, in_list_models
from core.api.fields import CacheChoiceField

class FSDJumpSerializer(BaseJournal):
    """
    sserializer dedicato alla lavorazione dei dati con scema journal e evento FSDJump
    """
    SystemEconomy = CustomCacheChoiceField(
        fun_choices=lambda: get_values_list_or_default(Economy, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
        cache_key=Economy.get_cache_key(),
        required=False,
        allow_blank=True,
    )
    SystemSecondEconomy = CustomCacheChoiceField(
        fun_choices=lambda: get_values_list_or_default(Economy, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
        cache_key=Economy.get_cache_key(),
        required=False,
        allow_blank=True,
    )
    SystemSecurity = CustomChoiceField(
        choices=[sc.lower() for sc in System.SecurityChoices.names],
        required=False,
    )
    Population = serializers.IntegerField(
        min_value=0,
    )
    Factions = serializers.ListField(
        child=MinorFactionInSystemSerializer(),
        required=False,
        min_length=0,
        max_length=MinorFactionInSystem.MaxRelation(),
    )
    SystemFaction = BaseMinorFactionSerializer(
        required=False,
    )
    #DEV: da implementare
    Conflicts = None
    Powers = serializers.ListField(
        child=CacheChoiceField(
            fun_choices=lambda: get_values_list_or_default(Power, [], (OperationalError, ProgrammingError), 'name', flat=True),
            cache_key=uuid.uuid4(),
        ),
        required=False,
        min_length=0,
        max_length=PowerInSystem.MaxRelation(),
    )
    PowerplayState = CacheChoiceField(
        fun_choices=lambda: get_values_list_or_default(PowerState, [], (OperationalError, ProgrammingError), 'eddn', 'name'),
        cache_key=uuid.uuid4(),
        required=False,
    )

    def validate(self, attrs):
        power = attrs.get('Powers', [])
        if power:
            state = attrs.get('PowerplayState', None)
            if state == PowerInSystem.StateForMoreRellation().eddn and len(power) < 1:
                raise serializers.ValidationError(
                    f'PowerplayState {state} require more than one power'
                )
            elif state != PowerInSystem.StateForMoreRellation().eddn and len(power) != 1:
                raise serializers.ValidationError(
                    f'PowerplayState {state} require only one power'
                )
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
        self.create_PowerInSystem(instance)

    def update_dipendent(self, instance):
        self.update_minor_faction(instance)
        self.check_control_faction(instance)
        self.update_PowerInSystem(instance)

    def update_or_create(self, validated_data: dict) -> System:
        self.data_preparation(validated_data)
        self.instance, create = create_or_update_if_time(
            System, time=self.get_time(), defaults=self.get_data_defaults(validated_data),
            defaults_create=self.get_data_defaults_create(), defaults_update=self.get_data_defaults_update(),
            update_function=self.update_dipendent, create_function=self.create_dipendent,
            name=validated_data.get('StarSystem'),
        )
        return self.instance
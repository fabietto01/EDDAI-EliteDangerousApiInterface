from rest_framework import serializers
from django.db import OperationalError, ProgrammingError
import uuid

from .BaseJournal import BaseJournal

from ..customFields import CustomChoiceField, CustomCacheChoiceField
from ..nestedSerializer import MinorFactionInSystemSerializer, BaseMinorFactionSerializer

from ed_system.models import System
from ed_economy.models import Economy
from ed_bgs.models import MinorFactionInSystem, MinorFaction, PowerInSystem, Power, PowerState

from core.utility import update_or_create_if_time, get_values_list_or_default, get_or_none
from django.db import OperationalError, ProgrammingError

from core.api.fields import CacheChoiceField

class FSDJumpSerializer(BaseJournal):
    """
    sserializer dedicato alla lavorazione dei dati con scema journal e evento FSDJump
    """
    SystemEconomy = CustomCacheChoiceField(
        fun_choices=lambda: get_values_list_or_default(Economy, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
        cache_key=uuid.uuid4(),
        required=False,
        allow_blank=True,
    )
    SystemSecondEconomy = CustomCacheChoiceField(
        fun_choices=lambda: get_values_list_or_default(Economy, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
        cache_key=uuid.uuid4(),
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
        max_length=MinorFactionInSystem.MaxRelation,
    )
    SystemFaction = BaseMinorFactionSerializer(
        required=False,
    )
    Conflicts = None
    Powers = serializers.ListField(
        child=CacheChoiceField(
            fun_choices=lambda: get_values_list_or_default(Power, [], (OperationalError, ProgrammingError), 'name', flat=True),
            cache_key=uuid.uuid4(),
        ),
        required=False,
        min_length=0,
        max_length=PowerInSystem.MaxRelation,
    )
    PowerplayState = CacheChoiceField(
        fun_choices=lambda: get_values_list_or_default(PowerState, [], (OperationalError, ProgrammingError), 'eddn', 'name'),
        cache_key=uuid.uuid4(),
        required=False,
    )

    def validate(self, attrs):
        power = attrs.get('Powers', [])
        if power:
            state = self.fields['PowerplayState'].choices.get(attrs.get('PowerplayState', None), None)
            if state in PowerInSystem.StateForMoreRellation and len(power) < 2:
                raise serializers.ValidationError(
                    f'PowerplayState {state} require more than one power'
                )
            elif not state in PowerInSystem.StateForMoreRellation and len(power) > 1:
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
        self.instance, create = update_or_create_if_time(
            System, time=self.get_time(), defaults=self.get_data_defaults(validated_data),
            update_function=self.update_dipendent, create_function=self.create_dipendent,
            name=validated_data.get('StarSystem'),
        )
        return self.instance
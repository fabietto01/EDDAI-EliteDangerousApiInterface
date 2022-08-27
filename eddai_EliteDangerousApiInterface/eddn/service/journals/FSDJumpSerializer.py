from rest_framework import serializers
from django.db import OperationalError, ProgrammingError

from eddn.service.journals.BaseJournal import BaseJournal

from eddn.service.seriallizers.customFields.CustomChoiceField import CustomChoiceField
from eddn.service.journals.MinorFaction import MinorFactionInSystemSerializer

from ed_system.models import System
from ed_economy.models import Economy
from ed_bgs.models import MinorFactionInSystem

from core.utility import update_or_create_if_time

class FSDJumpSerializer(BaseJournal):
    """
    sserializer dedicato alla lavorazione dei dati con scema journal e evento FSDJump
    """
    SystemEconomy = CustomChoiceField(
        choices=Economy().get_data_list(),
        required=False,
    )
    SystemSecondEconomy = CustomChoiceField(
        choices=Economy().get_data_list(),
        required=False,
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
    SystemFaction = None
    Conflicts = None
    Powers = None
    PowerplayState = None
    
    def set_data_defaults(self, validated_data: dict) -> dict:
        defaults = BaseJournal.set_data_defaults(self, validated_data)
        defaults.update(
            {
                "primaryEconomy": Economy().get_instanze_from_eddn(validated_data.get('SystemEconomy', None)),
                "secondaryEconomy": Economy().get_instanze_from_eddn(validated_data.get('SystemSecondEconomy', None)),
                "security": validated_data.get('SystemSecurity', None),
            }
        )
        return defaults

    def update_minor_faction(self, instance):
        for faction in self.factions_data:
            serializer = MinorFactionInSystemSerializer(data=faction)
            if serializer.is_valid():
                serializer.save(system=instance, timestamp=self.get_time())

    def data_preparation(self, validated_data: dict) -> dict:
        self.factions_data:dict = validated_data.pop("Factions", [])

    def create_dipendent(self, instance):
        self.update_minor_faction(instance)

    def update_dipendent(self, instance):
        self.update_minor_faction(instance)

    def update_or_create(self, validated_data: dict) -> System:
        self.data_preparation(validated_data)
        self.instance, create = update_or_create_if_time(
            System, time=self.get_time(), defaults=self.get_data_defaults(validated_data),
            update_function=self.update_dipendent, create_function=self.create_dipendent,
            name=validated_data.get('StarSystem'),
        )
        return self.instance
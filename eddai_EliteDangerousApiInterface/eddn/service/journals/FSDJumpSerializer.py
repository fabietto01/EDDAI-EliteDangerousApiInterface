from rest_framework import serializers
from django.db import OperationalError, ProgrammingError

from eddn.service.journals.BaseJournal import BaseJournal

from eddn.service.seriallizers.customFields.CustomChoiceField import CustomChoiceField

from ed_system.models import System
from ed_economy.models import Economy
from eddn.models import get_model_list_from_eddn

from core.utility import update_or_create_if_time, get_or_none

class FSDJumpSerializer(BaseJournal):
    """
    sserializer dedicato alla lavorazione dei dati con scema journal e evento FSDJump
    """
    SystemEconomy = CustomChoiceField(
        choices=get_model_list_from_eddn(Economy),
        required=False,
    )
    SystemSecondEconomy = CustomChoiceField(
        choices=get_model_list_from_eddn(Economy),
        required=False,
    )
    SystemSecurity = CustomChoiceField(
        choices=[sc.lower() for sc in System.SecurityChoices.names],
        required=False,
    )
    Population = serializers.IntegerField(
        min_value=0,
    )
    Factions = None
    SystemFaction = None
    Conflicts = None
    Powers = None
    PowerplayState = None
    
    def set_data_defaults(self, validated_data: dict) -> dict:
        defaults = BaseJournal.set_data_defaults(self, validated_data)
        defaults.update(
            {
                "primaryEconomy":    validated_data.get('SystemEconomy', None),
                "secondaryEconomy": validated_data.get('SystemSecondEconomy', None),
                "security": validated_data.get('SystemSecurity', None),
            }
        )
        return defaults

    def update_or_create(self, validated_data: dict) -> System:
        self.instance, create = update_or_create_if_time(
            System, time=self.get_time(), defaults=self.get_data_defaults(validated_data),
            name=validated_data.get('StarSystem'),
        )
        return self.instance
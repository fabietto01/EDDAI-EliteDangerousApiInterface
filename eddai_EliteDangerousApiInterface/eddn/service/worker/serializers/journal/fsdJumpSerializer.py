from .baseJournalSerializer import BaseJournalSerializer
from rest_framework import serializers

from ..customFields import SystemSecurityChoiceField, CoordinateListField
from ..nestedSerializers import MinorFactionInSystemSerializer, MinorFactionSerializer

from ed_economy.models import Economy
from ed_bgs.models import Power, PowerState, PowerInSystem
from ed_system.models import System

from core.utility import create_or_update_if_time

class FSDJumpSerializer(BaseJournalSerializer):
    SystemEconomy = serializers.SlugRelatedField(
        queryset=Economy.objects.all(),
        slug_field='eddn',
        required=False,
        allow_null=True,
        source="primaryEconomy"
    )
    SystemSecondEconomy = serializers.SlugRelatedField(
        queryset=Economy.objects.all(),
        slug_field='eddn',
        required=False,
        allow_null=True,
         source="secondaryEconomy"
    )
    SystemSecurity = SystemSecurityChoiceField(
        required=False,
        source="security"
    )
    Population = serializers.IntegerField(
        min_value=0,
        source="population"
    )
    Factions = MinorFactionInSystemSerializer(
        many=True, required=False,
        source="ed_bgs_MinorFactionInSystem_related"
    )

    def create(self, validated_data:dict):
        faction = validated_data.pop('ed_bgs_MinorFactionInSystem_related', None)
        instance = super().create(validated_data)
        if faction:
            serializers = MinorFactionInSystemSerializer(instance=instance, many=True)
            serializers._validated_data = faction
            serializers.save(
                created_by=validated_data.get('created_by'),
                updated_by=validated_data.get('created_by'),
            )
        return instance
    
    def update(self, instance, validated_data:dict):
        faction = validated_data.pop('ed_bgs_MinorFactionInSystem_related', None)
        instance = super().update(instance, validated_data)
        return instance

    class Meta:
        model = System
        fields = [
            'StarSystem', 'StarPos',
            "SystemEconomy", "SystemSecondEconomy",
            "SystemSecurity", "Population",
            "Factions",
            'timestamp',
        ]
from rest_framework import serializers
from ed_bgs.models import MinorFactionInSystem, MinorFaction

from .stateInMinorFactionSerializer import StateInMinorFactionBaseInformationSerializer

from ed_system.models import System

class MinorFactionInSystemBasicInformationSerializer(serializers.ModelSerializer):
    """Serializer for listing minor factions in system with basic information."""

    system = serializers.SlugRelatedField(
        queryset=System.objects.all(),
        slug_field='name',
    )
    minorFaction = serializers.SlugRelatedField(
        queryset=MinorFaction.objects.all(),
        slug_field='name',
    )

    class Meta:
        model = MinorFactionInSystem
        fields = [
            'id', 'system', 'minorFaction', 'Influence',
            'created_at', 'updated_at', 'created_by', 'updated_by',
        ]
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
        }

class MinorFactionInSystemSerializer(MinorFactionInSystemBasicInformationSerializer):
    """Serializer for detailed view of minor factions in system with states."""

    states = StateInMinorFactionBaseInformationSerializer(
        many=True, read_only=True,
        source='ed_bgs_stateinminorfaction_related'
    )

    class Meta(MinorFactionInSystemBasicInformationSerializer.Meta):
        fields = [
            'id', 'system', 'minorFaction', 'Influence', 'states',
            'created_at', 'updated_at', 'created_by', 'updated_by',
        ]


class MinorFactionInSystemFromMinorFactionSerializer(MinorFactionInSystemSerializer):
    class Meta(MinorFactionInSystemSerializer.Meta):
        fields = [
            'id', 'system', 'Influence', 'states',
            'created_at', 'updated_at', 'created_by', 'updated_by',
        ]


class MinorFactionInSystemFromsystemSerializer(MinorFactionInSystemSerializer):
    class Meta(MinorFactionInSystemSerializer.Meta):
        fields = [
            'id', 'minorFaction', 'Influence', 'states',
            'created_at', 'updated_at', 'created_by', 'updated_by',
        ]

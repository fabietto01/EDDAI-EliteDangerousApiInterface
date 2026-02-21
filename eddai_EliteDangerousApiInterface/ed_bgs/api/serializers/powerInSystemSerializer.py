from rest_framework import serializers
from ed_bgs.models import PowerInSystem, Power, PowerState
from ed_system.models import System


class PowerInSystemBasicInformationSerializer(serializers.ModelSerializer):
    """Serializer for listing power in system with basic information."""

    system = serializers.SlugRelatedField(
        queryset=System.objects.all(),
        slug_field='name',
    )
    power = serializers.SlugRelatedField(
        queryset=Power.objects.all(),
        slug_field='name',
    )
    state = serializers.SlugRelatedField(
        queryset=PowerState.objects.all(),
        slug_field='name',
    )

    class Meta:
        model = PowerInSystem
        fields = [
            'id', 'system', 'power', 'state',
            'created_at', 'updated_at', 'created_by', 'updated_by',
        ]
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
        }


class PowerInSystemSerializer(PowerInSystemBasicInformationSerializer):
    """Serializer for detailed view of power in system."""

    class Meta(PowerInSystemBasicInformationSerializer.Meta):
        fields = [
            'id', 'system', 'power', 'state',
            'created_at', 'updated_at', 'created_by', 'updated_by',
        ]


class PowerInSystemFromSystemSerializer(PowerInSystemSerializer):
    """Serializer for power in a specific system (used in nested endpoints)."""

    class Meta(PowerInSystemSerializer.Meta):
        fields = [
            'id', 'power', 'state',
            'created_at', 'updated_at', 'created_by', 'updated_by'
        ]


from rest_framework import serializers
from ed_body.models import Star, Planet, BaseBody, AtmosphereType

from .atmosphereComponentInPlanetSerializer import CompactedAtmosphereComponentInPlanetSerializer

from ed_system.api.serializers import SystemBasicInformation, System

class BaseBodySerializer(serializers.ModelSerializer):
    """
    BaseBodySerializer is a serializer for the BaseBody model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """

    system = SystemBasicInformation(read_only=True)
    system_id = serializers.PrimaryKeyRelatedField(
        queryset=System.objects.all(),
        write_only=True,
        source='system',
    )

    class Meta:
        model = BaseBody
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
        }
        fields = "__all__"


class StarSerializer(BaseBodySerializer):
    """
    StarSerializer is a serializer for the Star model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """
    class Meta(BaseBodySerializer.Meta):
        model = Star

class PlanetSerializer(BaseBodySerializer):
    """
    PlanetSerializer is a serializer for the Planet model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """

    atmosphere_component = CompactedAtmosphereComponentInPlanetSerializer(
        many=True,
        source='ed_body_atmospherecomponentinplanet_related'
    )
    atmosphereType = serializers.SlugRelatedField(
        queryset=AtmosphereType.objects.all(),
        slug_field='name'
    )

    class Meta(BaseBodySerializer.Meta):
        model = Planet
        fields = "__all__"
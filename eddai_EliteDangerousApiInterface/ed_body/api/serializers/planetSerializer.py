from rest_framework import serializers
from .baseBodySerializer import BaseBodySerializer

from ed_core.api.serializers.DistanceSerializer import DistanceSerializer
from .atmosphereComponentInPlanetSerializer import CompactedAtmosphereComponentInPlanetSerializer

from ed_body.models import (
    Planet, AtmosphereType, PlanetType, Volcanism
)

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
    planetType = serializers.SlugRelatedField(
        queryset=PlanetType.objects.all(),
        slug_field='name'
    )
    volcanism = serializers.SlugRelatedField(
        queryset=Volcanism.objects.all(),
        slug_field='name'
    )

    class Meta(BaseBodySerializer.Meta):
        model = Planet

class PlanetDistanceSerializer(PlanetSerializer, DistanceSerializer):
    class Meta(PlanetSerializer.Meta):
        pass
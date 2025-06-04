from rest_framework import serializers
from .baseBodySerializer._baseBodySerializer import _BaseBodySerializer

from ed_core.api.serializers.DistanceSerializer import DistanceSerializer
from .atmosphereComponentInPlanetSerializer import CompactedAtmosphereComponentInPlanetSerializer

from ed_body.models import (
    Planet, AtmosphereType, PlanetType, Volcanism
)

class PlanetSerializer(_BaseBodySerializer):
    """
    PlanetSerializer is a serializer for the Planet model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """

    class CompositionSerializer(serializers.Serializer):

        ice = serializers.FloatField(source='_compositionIce')
        rock = serializers.FloatField(source='_compositionRock')
        metal = serializers.FloatField(source='_compositionMetal')
        
    atmosphere_component = CompactedAtmosphereComponentInPlanetSerializer(
        many=True,
        source='ed_body_atmospherecomponentinplanet_related',
        required=False
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
    composition = CompositionSerializer(source='*', required=False)

    class Meta(_BaseBodySerializer.Meta):
        model = Planet
        fields = None
        exclude = [
            "_compositionIce", "_compositionRock",
            "_compositionMetal"
        ]

class PlanetDistanceSerializer(PlanetSerializer, DistanceSerializer):
    class Meta(PlanetSerializer.Meta):
        pass
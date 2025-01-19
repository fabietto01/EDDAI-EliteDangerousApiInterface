from rest_framework import serializers

from ed_body.models import PlanetType

class CompactedPlanetTypeSerializer(serializers.ModelSerializer):
    """
    PlanetTypeSerializer is a serializer for the PlanetType model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """

    class Meta:
        model = PlanetType
        fields = ['id', 'name']

class PlanetTypeSerializer(CompactedPlanetTypeSerializer):
    """
    PlanetTypeSerializer is a serializer for the PlanetType model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """

    class Meta(CompactedPlanetTypeSerializer.Meta):
        fields = "__all__"
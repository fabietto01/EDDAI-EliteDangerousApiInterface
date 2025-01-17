from rest_framework import serializers

from ed_body.models import AtmosphereComponent

class CompactedAtmosphereComponentSerializer(serializers.ModelSerializer):
    """
    CompactedAtmosphereComponentSerializer is a serializer for the AtmosphereComponent model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """

    class Meta:
        model = AtmosphereComponent
        fields = ['id', 'name']

class AtmosphereComponentSerializer(CompactedAtmosphereComponentSerializer):
    """
    AtmosphereComponentSerializer is a serializer for the AtmosphereComponent model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """

    class Meta(CompactedAtmosphereComponentSerializer.Meta):
        fields = None
        exclude  = ['_eddn', 'eddn']

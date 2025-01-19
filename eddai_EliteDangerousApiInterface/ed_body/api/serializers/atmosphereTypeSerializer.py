from rest_framework import serializers

from ed_body.models import AtmosphereType

class CompactedAtmosphereTypeSerializer(serializers.ModelSerializer):
    """
    CompactedAtmosphereTypeSerializer is a serializer for the AtmosphereType model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """

    class Meta:
        model = AtmosphereType
        fields = ['id', 'name']


class AtmosphereTypeSerializer(CompactedAtmosphereTypeSerializer):
    """
    AtmosphereTypeSerializer is a serializer for the AtmosphereType model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """

    class Meta(CompactedAtmosphereTypeSerializer.Meta):
        fields = None
        exclude = ['_eddn', 'eddn']
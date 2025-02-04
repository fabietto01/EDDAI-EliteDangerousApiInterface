from rest_framework import serializers

from ed_body.models import StarType

class CompactedStarTypeSerializer(serializers.ModelSerializer):
    """
    CompactedStarTypeSerializer is a serializer for the StarType model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """

    class Meta:
        model = StarType
        fields = ['id', 'name']

class StarTypeSerializer(CompactedStarTypeSerializer):
    """
    StarTypeSerializer is a serializer for the StarType model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """

    class Meta(CompactedStarTypeSerializer.Meta):
        fields = None
        exclude = ['_eddn', 'eddn']
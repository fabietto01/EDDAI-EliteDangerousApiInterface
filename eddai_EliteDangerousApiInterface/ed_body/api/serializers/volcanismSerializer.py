from rest_framework import serializers

from ed_body.models import Volcanism

class CompactedVolcanismSerializer(serializers.ModelSerializer):
    """
    CompactedVolcanismSerializer is a serializer for the Volcanism model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """

    class Meta:
        model = Volcanism
        fields = ['id', 'name']

class VolcanismSerializer(CompactedVolcanismSerializer):
    """
    VolcanismSerializer is a serializer for the Volcanism model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """

    class Meta(CompactedVolcanismSerializer.Meta):
        fields = None
        exclude = ['_eddn', 'eddn']
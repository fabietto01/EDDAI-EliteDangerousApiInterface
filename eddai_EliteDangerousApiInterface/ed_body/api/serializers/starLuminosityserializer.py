from rest_framework import serializers

from ed_body.models import StarLuminosity

class CompactedStarLuminositySerializer(serializers.ModelSerializer):
    """
    CompactedStarLuminositySerializer is a serializer for the StarLuminosity model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """

    class Meta:
        model = StarLuminosity
        fields = ['id', 'name']

class StarLuminositySerializer(CompactedStarLuminositySerializer):
    """
    StarLuminositySerializer is a serializer for the StarLuminosity model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """

    class Meta(CompactedStarLuminositySerializer.Meta):
        fields = "__all__"
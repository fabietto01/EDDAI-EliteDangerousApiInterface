from rest_framework import serializers

from ed_material.models import Material

class CompactedMaterialSerializer(serializers.ModelSerializer):
    """
    CompactedMaterialSerializer is a serializer for the Material model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """

    class Meta:
        model = Material
        fields = ['id', 'name']

class MaterialSerializer(CompactedMaterialSerializer):
    """
    MaterialSerializer is a serializer for the Material model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """

    class Meta(CompactedMaterialSerializer.Meta):
        fields = None
        exclude  = ['_eddn', 'eddn']

from rest_framework import serializers

from ed_material.models import Material

class CompactedMaterialSerializer(serializers.ModelSerializer):

    class Meta:
        model = Material
        fields = ['id', 'name']

class BaseMaterialSerializer(CompactedMaterialSerializer):

    class Meta(CompactedMaterialSerializer.Meta):
        fields = None
        exclude = ['_eddn', 'eddn', 'note']

class MaterialSerializer(BaseMaterialSerializer):

    class Meta(BaseMaterialSerializer.Meta):
        exclude = ['_eddn', 'eddn']

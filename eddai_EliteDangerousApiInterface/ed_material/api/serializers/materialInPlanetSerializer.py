from rest_framework import serializers
from django.shortcuts import get_object_or_404
from django.db.models import Sum

from ed_material.models import Material, MaterialInPlanet
from ed_body.models import Planet
from .materialSerializer import CompactedMaterialSerializer

class ListMaterialInPlanetSerializer(serializers.ListSerializer):

    def create(self, validated_data):
        instances = [MaterialInPlanet(**item) for item in validated_data]
        return MaterialInPlanet.objects.bulk_create(instances)


class CompactedMaterialInPlanetSerializer(serializers.ModelSerializer):
    """
    Serializer per MaterialInPlanet con dettagli completi del materiale
    """
    material = CompactedMaterialSerializer(read_only=True)

    class Meta:
        model = MaterialInPlanet
        read_only_fields = [
            'created_at','updated_at',
            'created_by','updated_by',
            'id'
        ]
        fields = ['id', 'material', 'percent']
    
    def validate(self, attrs):
        try:
            if attrs['material'].type != Material.MaterialType.RAW.value:
                raise serializers.ValidationError("Solo i materiali di tipo RAW possono essere associati ai pianeti.")
        except KeyError:
            from rest_framework import status
            raise serializers.ValidationError('An internal server error occurred', code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return attrs

class MaterialInPlanetSerializer(CompactedMaterialInPlanetSerializer):
    """
    MaterialInPlanetSerializer è un serializer per il modello MaterialInPlanet.
    Attributi:
        Meta (type): La classe di metadati per il serializer.
    """

    material_id = serializers.PrimaryKeyRelatedField(
        queryset=Material.objects.filter(type=Material.MaterialType.RAW.value),
        source='material',
        write_only=True
    )

    class Meta(CompactedMaterialInPlanetSerializer.Meta):
        model = MaterialInPlanet
        fields = None
        exclude = ['planet']
        read_only_fields = [
            'created_at','updated_at',
            'created_by','updated_by',
            'planet', 'id'
        ]
        list_serializer_class = ListMaterialInPlanetSerializer
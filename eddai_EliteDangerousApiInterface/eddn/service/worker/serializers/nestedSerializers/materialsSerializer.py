from ..baseSerializer import BaseSerializer
from rest_framework import serializers

from core.utility import (
    create_or_update_if_time, in_list_models, 
)

from ed_material.models import Material, MaterialInPlanet

class MaterialsSerializerListSerializer(serializers.ListSerializer):

    def _get_plante(self):
        return self.context.get('planet')

    def create(self, validated_data):
        materials_in_planet_add = []
        materials_in_planet_delete = []
        materials_in_planet_qs_list = list(MaterialInPlanet.objects.filter(planet=self._get_plante()))
        materials = [MaterialInPlanet(**item) for item in validated_data]
        for material in materials:
            if not in_list_models(material, materials_in_planet_qs_list):
                materials_in_planet_add.append(material)
        for material in materials_in_planet_qs_list:
            if not in_list_models(material, materials):
                materials_in_planet_delete.append(material.id)
        if materials_in_planet_delete:
            MaterialInPlanet.objects.filter(id__in=materials_in_planet_delete).delete()
        if materials_in_planet_add:
            materials = MaterialInPlanet.objects.bulk_create(materials_in_planet_add)
        return materials
    
class MaterialsSerializer(BaseSerializer):
    Name = serializers.SlugRelatedField(
        queryset=Material.objects.filter(type=Material.MaterialType.RAW.value),
        slug_field='eddn',
        source='material',
    )
    Percent = serializers.FloatField(
        min_value=0,
        max_value=100,
        source='percent',
    )

    class Meta:
        list_serializer_class = MaterialsSerializerListSerializer
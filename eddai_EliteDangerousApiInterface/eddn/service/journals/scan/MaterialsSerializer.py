from rest_framework import serializers
from eddn.service.seriallizers.BaseSerializer import BaseSerializer

from core.utility import update_or_create_if_time, get_values_list_or_default, get_or_none
from django.db import OperationalError, ProgrammingError

from ed_body.models import Planet, MaterialInPlanet
from ed_material.models.Material import Material

class MaterialsSerializer(BaseSerializer):
    Name = serializers.ChoiceField(
        choices=get_values_list_or_default(Material.objects.filter(type=Material.MaterialType.RAW.label), [], (OperationalError, ProgrammingError), 'name', flat=True)
    )
    Percent = serializers.FloatField(
        min_value=0,
        max_value=100,
    )

    def set_data_defaults(self, validated_data: dict) -> dict:
        return {
            'percent': validated_data.get('Percent'),
        }

    def update_or_create(self, validated_data: dict) -> MaterialInPlanet:
        materialInPlanet, created = update_or_create_if_time(
            MaterialInPlanet, time=self.get_time(validated_data), defaults=self.get_data_defaults(validated_data),
            planet=validated_data.get('planet'), material=validated_data.get('material')
        )
        return materialInPlanet
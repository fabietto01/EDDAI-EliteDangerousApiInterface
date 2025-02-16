from ..baseSerializer import BaseSerializer
from rest_framework import serializers

from core.utility import (
    create_or_update_if_time, in_list_models, 
)

from ed_body.models import AtmosphereComponentInPlanet, AtmosphereComponent

class AtmosphereComponentListSerializer(serializers.ListSerializer):

    def _get_plante(self, validated_data):
        return validated_data[0].get('planet')

    def create(self, validated_data):
        plante = self._get_plante(validated_data)
        atmosphere_component_in_planet_add = []
        atmosphere_component_in_planet_delete = []
        atmosphere_component_in_planet__qs_list = list(AtmosphereComponentInPlanet.objects.filter(planet=plante))
        atmosphere_component_in_planet = [AtmosphereComponentInPlanet(**item) for item in validated_data]
        for atmosphereComponent in atmosphere_component_in_planet:
            if not in_list_models(atmosphereComponent, atmosphere_component_in_planet__qs_list):
                atmosphere_component_in_planet_add.append(atmosphereComponent)
        for atmosphereComponent in atmosphere_component_in_planet__qs_list:
            if not in_list_models(atmosphereComponent, atmosphere_component_in_planet):
                atmosphere_component_in_planet_delete.append(atmosphereComponent.id)
        if atmosphere_component_in_planet_delete:
            AtmosphereComponentInPlanet.objects.filter(id__in=atmosphere_component_in_planet_delete).delete()
        if atmosphere_component_in_planet_add:
            atmosphere_component_in_planet = AtmosphereComponentInPlanet.objects.bulk_create(atmosphere_component_in_planet_add)
        return atmosphere_component_in_planet

class AtmosphereComponentSerializer(BaseSerializer):
    Name = serializers.SlugRelatedField(
        queryset=AtmosphereComponent.objects.all(),
        slug_field='eddn',
        source='atmosphere_component',
    )
    Percent = serializers.FloatField(
        min_value=0,
        max_value=100,
        source='percent',
    )

    class Meta:
        list_serializer_class = AtmosphereComponentListSerializer
from rest_framework import serializers
from eddn.service.serializer.nestedSerializer.BaseSecondarySerializer import BaseNestedSerializer

from core.utility import create_or_update_if_time, get_or_none

from core.api.fields import CacheSlugRelatedField
from ed_body.models import AtmosphereComponentInPlanet, AtmosphereComponent

class AtmosphereComponentSerializer(BaseNestedSerializer):
    Name = CacheSlugRelatedField(
        queryset=AtmosphereComponent.objects.all(),
        slug_field='eddn',
    )
    Percent = serializers.FloatField(
        min_value=0,
        max_value=100,
    )

    def set_data_defaults(self, validated_data: dict) -> dict:
        return {
            'percent': validated_data.get('Percent'),
        }

    def update_or_create(self, validated_data: dict) -> AtmosphereComponentInPlanet:
        atmosphereComponentInPlanet, created = create_or_update_if_time(
            AtmosphereComponentInPlanet, time=self.get_time(validated_data), defaults=self.get_data_defaults(validated_data),
            planet=validated_data.get('planet'), atmosphereComponent=get_or_none(AtmosphereComponent, eddn=validated_data.get('Name'))
        )
        return atmosphereComponentInPlanet
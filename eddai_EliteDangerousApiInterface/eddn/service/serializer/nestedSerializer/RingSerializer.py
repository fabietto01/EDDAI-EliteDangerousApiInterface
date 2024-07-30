from rest_framework import serializers
from .BaseSecondarySerializer import BaseNestedSerializer

from ..customFields import RingClassmChoiceField

from core.utility import create_or_update_if_time
from ed_mining.models import Ring

class RingSerializer(BaseNestedSerializer):

    Name = serializers.CharField(
        max_length=255,
    )
    RingClass = RingClassmChoiceField(
        choices=Ring.RingType.choices,
    )
    MassMT = serializers.FloatField(
        min_value=0,
    )
    InnerRad = serializers.FloatField(
        min_value=0,
    )
    OuterRad = serializers.FloatField(
        min_value=0,
    )

    def set_data_defaults(self, validated_data: dict) -> dict:
        return {
            'ringType': validated_data.get('RingClass'),
            'massMT': validated_data.get('MassMT'),
            'innerRad': validated_data.get('InnerRad'),
            'outerRad': validated_data.get('OuterRad'),
        }

    def update_or_create(self, validated_data: dict) -> Ring:
        ring, created = create_or_update_if_time(
            Ring, time=self.get_time(validated_data), defaults=self.get_data_defaults(validated_data),
            defaults_create=self.get_data_defaults_create(), defaults_update=self.get_data_defaults_update(),
            body=validated_data.get('body'), name=validated_data.get('Name')
        )
        return ring
    
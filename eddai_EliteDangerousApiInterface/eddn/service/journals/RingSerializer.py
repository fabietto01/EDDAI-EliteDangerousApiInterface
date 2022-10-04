from rest_framework import serializers
from eddn.service.seriallizers.BaseSerializer import BaseSerializer

from eddn.service.seriallizers.customFields.CustomChoiceField import RingClassmChoiceField

from core.utility import update_or_create_if_time, get_values_list_or_default, get_or_none
from ed_body.models import Ring

class RingSerializer(BaseSerializer):

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
        ring, created = update_or_create_if_time(
            Ring, time=self.get_time(validated_data), defaults=self.get_data_defaults(validated_data),
            body=validated_data.get('body'), name=validated_data.get('Name')
        )
        return ring
    
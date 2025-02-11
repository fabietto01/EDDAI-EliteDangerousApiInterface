from ..baseSerializer import BaseSerializer
from rest_framework import serializers

from ..customFields import RingTypeChoiceField
from core.utility import create_or_update_if_time
from ed_mining.models import Ring

class RingListSerializer(serializers.ListSerializer):

    def validate(self, attrs):
        count = len(attrs)
        if count < 1:
            raise serializers.ValidationError(f"too few rings: {count}")
        return super().validate(attrs)

class RingSerializer(BaseSerializer):
    Name = serializers.CharField(
        max_length=255,
    )
    RingClass = RingTypeChoiceField()
    MassMT = serializers.FloatField(
        min_value=0,
    )
    InnerRad = serializers.FloatField(
        min_value=0,
    )
    OuterRad = serializers.FloatField(
        min_value=0,
    )

    def set_data_defaults(self, validated_data):
        return {
            'ringType': validated_data.get('RingClass'),
            'massMT': validated_data.get('MassMT'),
            'innerRad': validated_data.get('InnerRad'),
            'outerRad': validated_data.get('OuterRad'),
        }
    
    def set_data_defaults_create(self, validated_data):
        return {
            "created_by": validated_data.get('created_by'),
            "updated_by": validated_data.get('updated_by'),
            "updated_at": validated_data.get('updated_at'),
            "created_at": validated_data.get('updated_at'),
        }

    def set_data_defaults_update(self, validated_data):
        return {
            "updated_by": validated_data.get('updated_by'),
            "updated_at": validated_data.get('updated_at'),
        }
    
    def update_or_create(self, validated_data):
        ring, created = create_or_update_if_time(
            Ring, time=self.get_time(validated_data), defaults=self.get_data_defaults(validated_data),
            defaults_create=self.get_data_defaults_create(validated_data), defaults_update=self.get_data_defaults_update(validated_data),
            body=validated_data.get('body'), name=validated_data.get('Name')
        )
        return ring
    
    class Meta:
        list_serializer_class = RingListSerializer
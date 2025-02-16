from ..baseSerializer import BaseSerializer
from rest_framework import serializers
from ..customFields import  CoordinateListField

from ed_system.models import System

from core.utility import create_or_update_if_time

class BaseJournalSerializer(BaseSerializer):
    StarSystem = serializers.CharField(
        min_length=1,
    )
    StarPos = CoordinateListField(
        source='coordinate',
    )
    timestamp = serializers.DateTimeField(
        input_formats=[
            "%Y-%m-%dT%H:%M:%SZ"
        ],
        source="updated_at"
    )

    def set_data_defaults(self, validated_data:dict) -> dict:
        return {
            "coordinate": validated_data.get('coordinate'),
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

    def update_or_create(self, validated_data:dict, update_function=None, create_function=None) -> System:
        sytsem, create = create_or_update_if_time(
            System, time=self.get_time(),
            defaults=self.get_data_defaults(validated_data),
            defaults_update=self.get_data_defaults_update(validated_data),
            defaults_create=self.get_data_defaults_create(validated_data),
            update_function=update_function,
            create_function=create_function,
            name=validated_data.get('StarSystem'),
        )
        return sytsem
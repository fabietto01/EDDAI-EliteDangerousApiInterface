from rest_framework import serializers
from ed_system.models import System
from eddn.service.seriallizers.BaseSerializer import BaseSerializer

from core.utility import update_or_create_if_time

class BaseJournal(BaseSerializer):
    StarPos = serializers.ListField(
        child=serializers.FloatField(),
        min_length=3,
        max_length=3,
    )
    StarSystem = serializers.CharField(
        min_length=1
    )
    timestamp = serializers.DateTimeField(
        input_formats=[
            "%Y-%m-%dT%H:%M:%SZ"
        ]
    )

    def set_data_defaults(self, validated_data:dict) -> dict:
        x,y,z = validated_data.get('StarPos')
        return {
            "x": x,
            "y": y,
            "z": z,
        }

    def update_or_create(self, validated_data:dict, update_function=None, create_function=None) -> System:
        sytsem, create = update_or_create_if_time(
            System, time=self.get_time(),
            defaults=self.get_data_defaults(validated_data),
            update_function=update_function,
            create_function=create_function,
            name=validated_data.get('StarSystem'),
        )
        return sytsem
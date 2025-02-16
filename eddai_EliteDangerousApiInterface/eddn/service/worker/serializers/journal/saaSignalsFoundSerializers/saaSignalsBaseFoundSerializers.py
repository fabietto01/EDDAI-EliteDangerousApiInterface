from ..baseJournalSerializer import BaseJournalSerializer
from rest_framework import serializers

from core.utility import create_or_update_if_time

class SAASignalsBaseFoundSerializers(BaseJournalSerializer):
    BodyName = serializers.CharField(
        min_length=1,
        max_length=255,
    )
    BodyID = serializers.IntegerField(
        min_value=0,
    )
    Signals = None

    def _get_body_name(self, validated_data):
        raise NotImplementedError('set_data_defaults must be implemented in child class')
    
    def _get_class_body(self, validated_data):
        raise NotImplementedError('set_data_defaults must be implemented in child class')

    def set_data_defaults_body(self, validated_data):
        return {
            'name': self._get_body_name(validated_data)
        }

    def update_or_create(self, validated_data, update_function=None, create_function=None):
        system = super().update_or_create(validated_data)
        palent, create = create_or_update_if_time(
            self._get_class_body(validated_data), time=self.get_time(),
            defaults=self.get_data_defaults(validated_data, self.set_data_defaults_body),
            defaults_create=self.get_data_defaults_create(validated_data),
            defaults_update=self.get_data_defaults_update(validated_data),
            update_function=update_function,
            create_function=create_function,
            bodyID=validated_data.get('BodyID'),
            system=system
        )
        return palent
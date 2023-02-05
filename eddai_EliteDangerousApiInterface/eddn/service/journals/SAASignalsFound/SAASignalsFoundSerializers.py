from rest_framework import serializers
from eddn.service.journals.BaseJournal import BaseJournal

from core.utility import update_or_create_if_time


class SAASignalsFoundSerializers(BaseJournal):
    BodyName = serializers.CharField(
        min_length=1
    )
    BodyID = serializers.IntegerField(
        min_value=0
    )
    Signals = None

    def set_data_defaults(self, validated_data: dict) -> dict:
        raise NotImplementedError('set_data_defaults must be implemented in child class')

    def set_data_defaults_system(self, validated_data: dict) -> dict:
        return super(SAASignalsFoundSerializers, self).set_data_defaults(validated_data)

    def update_dipendent(self, instance):
        pass

    def create_dipendent(self, instance):
        pass

    def data_preparation(self, validated_data: dict) -> dict:
        self.signals:list[dict] = validated_data.get('Signals', None)

    def update_or_create(self, validated_data: dict, *args, **kwargs):
        self.data_preparation(validated_data)
        self.initial, create = update_or_create_if_time(
            self.Meta.model, time=self.get_time(), defaults=self.get_data_defaults(validated_data),
            create_function=self.create_dipendent, update_function=self.update_dipendent,
            name=validated_data.get('BodyName'), *args, **kwargs
        )
        return self.initial
    
    class Meta:
        model = NotImplemented
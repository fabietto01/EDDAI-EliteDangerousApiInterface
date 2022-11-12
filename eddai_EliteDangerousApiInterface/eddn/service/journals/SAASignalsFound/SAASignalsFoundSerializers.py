from rest_framework import serializers
from eddn.service.journals.BaseJournal import BaseJournal

from ed_body.models import BaseBody
from ed_system.models import System

from core.utility import update_or_create_if_time, get_values_list_or_default, get_or_none

class SAASignalsFoundSerializers(BaseJournal):
    BodyName = serializers.CharField(
        min_length=1
    )
    BodyID = serializers.IntegerField(
        min_value=0
    )
    Signals = None

    def set_data_defaults(self, validated_data: dict) -> dict:
        return {}

    def update_dipendence(self, instance):
        pass

    def create_dipendence(self, instance):
        pass

    def data_preparation(self, validated_data: dict) -> dict:
        self.signals:list[dict] = validated_data.get('Signals', None)

    def update_or_create(self, validated_data: dict):
        self.data_preparation(validated_data)
        self.initial, create = update_or_create_if_time(
            self.Meta.model, time=self.get_time(), defaults=self.get_data_defaults(validated_data),
            create_function=self.create_dipendence, update_function=self.update_dipendence,
            name=validated_data.get('BodyName')   
        )
        return self.initial
    
    class Meta:
        model = NotImplemented
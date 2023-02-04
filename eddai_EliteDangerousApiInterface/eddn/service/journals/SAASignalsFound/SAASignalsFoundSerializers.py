from rest_framework import serializers
from eddn.service.journals.BaseJournal import BaseJournal

from ed_body.models import BaseBody
from ed_system.models import System

from core.utility import update_or_create_if_time

import re

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

    def set_data_defaults_body(self, validated_data: dict) -> dict:
        return {
            'bodyID': validated_data.get('BodyID')
        }

    def update_dipendence(self, instance):
        pass

    def create_dipendence(self, instance):
        pass

    def data_preparation(self, validated_data: dict) -> dict:
        self.signals:list[dict] = validated_data.get('Signals', None)

    def update_or_create(self, validated_data: dict):
        self.systemInstance, create = update_or_create_if_time(
            System, time=self.get_time(),
            defaults=self.get_data_defaults(validated_data, self.set_data_defaults_system),
            name=validated_data.get('StarSystem'),
        )
        bodyName = re.sub(
            r"\s[A-Z]\sRing$", "", validated_data.get('BodyName'), 0, 
        )
        self.bodyInstance, created = update_or_create_if_time(
            BaseBody, time=self.get_time(), 
            defaults=self.get_data_defaults(validated_data, self.set_data_defaults_body),
            name=bodyName, system=self.systemInstance
        )
        self.data_preparation(validated_data)
        self.initial, create = update_or_create_if_time(
            self.Meta.model, time=self.get_time(), defaults=self.get_data_defaults(validated_data),
            create_function=self.create_dipendence, update_function=self.update_dipendence,
            name=validated_data.get('BodyName'), 
        )
        return self.initial
    
    class Meta:
        model = NotImplemented
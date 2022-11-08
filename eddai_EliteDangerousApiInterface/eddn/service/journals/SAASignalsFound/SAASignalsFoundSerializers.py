from rest_framework import serializers
from eddn.service.journals.BaseJournal import BaseJournal

from core.utility import update_or_create_if_time, get_values_list_or_default, get_or_none

class SAASignalsFoundSerializers(BaseJournal):
    BodyName = serializers.CharField(
        min_length=1
    )
    BodyID = serializers.IntegerField(
        min_value=0
    )
    Signals = None

    def update_or_create(self, validated_data: dict, update_function=None, create_function=None):
        self.initial, create = update_or_create_if_time(
            self.Meta.model, time=self.get_time(), defaults=self.get_data_defaults(validated_data),
        )   
        return self.initial
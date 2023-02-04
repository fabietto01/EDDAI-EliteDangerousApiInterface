from rest_framework import serializers
from django.db import OperationalError, ProgrammingError
from eddn.service.journals.SAASignalsFound.SAASignalsFoundSerializers import (
    SAASignalsFoundSerializers,
    update_or_create_if_time,
)

from core.utility import  get_values_list_or_default

from ed_exploration.models import Signal, SignalSignals, Sample, SampleSignals
from ed_body.models import BaseBody

class SignalSerializers(serializers.Serializer):
    Type = serializers.ChoiceField(
        choices=get_values_list_or_default(SignalSignals, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
    )
    Count = serializers.IntegerField(
        min_value=0,
    )

class SampleSerializers(serializers.Serializer):
    Type = serializers.ChoiceField(
        choices=get_values_list_or_default(SampleSignals, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
    )

class SAASignalsFoundSignalAndSampleSerializers(SAASignalsFoundSerializers):
    """	
    """	
    Signals = serializers.ListField(
        child=SignalSerializers(),
        min_length=1
    )
    Genuses = serializers.ListField(
        child=SampleSerializers(),
        required=False,
        min_length=1
    )




    class Meta:
        model = BaseBody


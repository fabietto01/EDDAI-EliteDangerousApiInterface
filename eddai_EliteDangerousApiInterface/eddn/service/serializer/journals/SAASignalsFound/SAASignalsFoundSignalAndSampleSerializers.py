from rest_framework import serializers
from django.db import OperationalError, ProgrammingError
from eddn.service.seriallizers.journals.SAASignalsFound.SAASignalsFoundSerializers import SAASignalsFoundSerializers

from core.utility import  get_values_list_or_default, in_list_models, update_or_create_if_time

from ed_exploration.models import Signal, SignalSignals, Sample, SampleSignals
from ed_body.models import Planet
from ed_system.models import System

class SignalSerializers(serializers.Serializer):
    Type = serializers.ChoiceField(
        choices=get_values_list_or_default(SignalSignals, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
    )
    Count = serializers.IntegerField(
        min_value=0,
    )

class SampleSerializers(serializers.Serializer):
    Genus = serializers.ChoiceField(
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

    def set_data_defaults(self, validated_data: dict) -> dict:
        return {
            'bodyID': validated_data.get('BodyID'),
        }

    def update_dipendent_signals(self, instance):
        signalcreate:list[Signal] = []
        signaldelete:list[Signal] = []
        signalqs = Signal.objects.filter(planet=instance)
        signalqsList = list(signalqs)
        signalList = [
            Signal(
                planet=instance, type=SignalSignals.objects.get(eddn=signal.get('Type')), 
                count=signal.get('Count')
            ) for signal in self.signals
        ]
        for signal in signalList:
            if not in_list_models(signal, signalqsList, ['id','pk','updated']):
                signalcreate.append(signal)
        for signal in signalqsList:
            if not in_list_models(signal, signalList, ['id','pk','updated']):
                signaldelete.append(signal)
        if signalcreate:
            Signal.objects.bulk_create(signalcreate)
        if signaldelete:
            Signal.objects.filter(pk__in=[signal.pk for signal in signaldelete]).delete()

    def update_dipendent_genuses(self, instance):
        samplecreate:list[Sample] = []
        sampledelete:list[Sample] = []
        sampleqs = Sample.objects.filter(planet=instance)
        sampleqsList = list(sampleqs)
        sampleList = [
            Sample(
                planet=instance, type=SampleSignals.objects.get(eddn=sample.get('Genus'))
            ) for sample in self.genuses
        ]
        for sample in sampleList:
            if not in_list_models(sample, sampleqsList, ['id','pk','updated']):
                samplecreate.append(sample)
        for sample in sampleqsList:
            if not in_list_models(sample, sampleList, ['id','pk','updated']):
                sampledelete.append(sample)
        if samplecreate:
            Sample.objects.bulk_create(samplecreate)
        if sampledelete:
            Sample.objects.filter(pk__in=[sample.pk for sample in sampledelete]).delete()

    def update_dipendent(self, instance):
        self.update_dipendent_signals(instance)
        if self.genuses:
            self.update_dipendent_genuses(instance)

    def create_dipendent(self, instance):
        signalcreate = [
            Signal(
                planet=instance, type=SignalSignals.objects.get(eddn=signal.get('Type')), 
                count=signal.get('Count')
            ) for signal in self.signals
        ]
        Signal.objects.bulk_create(signalcreate)
        if self.genuses:
            samplecreate = [
                Sample(
                    planet=instance, type=SampleSignals.objects.get(eddn=sample.get('Genus'))
                ) for sample in self.genuses
            ]
            Sample.objects.bulk_create(samplecreate)

    def data_preparation(self, validated_data: dict) -> dict:
        super().data_preparation(validated_data)
        self.genuses = validated_data.get('Genuses', [])

    def update_or_create(self, validated_data: dict, *args, **kwargs):
        systemInstance, create = update_or_create_if_time(
            System, time=self.get_time(), 
            defaults=self.get_data_defaults(validated_data, self.set_data_defaults_system),
            name=validated_data.get('StarSystem')
        )
        return super().update_or_create(validated_data, system=systemInstance)

    class Meta:
        model = Planet
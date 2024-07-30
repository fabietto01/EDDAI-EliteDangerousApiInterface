from rest_framework import serializers
from django.db import OperationalError, ProgrammingError
from eddn.service.serializer.journals.SAASignalsFound.SAASignalsFoundSerializers import SAASignalsFoundSerializers

from core.utility import  get_values_list_or_default, in_list_models, create_or_update_if_time
from core.api.fields import CacheChoiceField

from ed_exploration.models import Signal, SignalSignals, Sample, SampleSignals
from ed_body.models import Planet
from ed_system.models import System

class SignalSerializers(serializers.Serializer):
    Type = CacheChoiceField(
        fun_choices=lambda: get_values_list_or_default(SignalSignals, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
        cache_key=SignalSignals.get_cache_key("eddn", flat=True),
    )
    Count = serializers.IntegerField(
        min_value=0,
    )

class SampleSerializers(serializers.Serializer):
    Genus = CacheChoiceField(
        fun_choices=lambda: get_values_list_or_default(SampleSignals, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
        cache_key=SampleSignals.get_cache_key("eddn", flat=True),
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
        signaldelete:list[int] = []
        signalqs = Signal.objects.filter(planet=instance)
        signalList = [
            Signal(
                planet=instance, type=SignalSignals.objects.get(eddn=signal.get('Type')), 
                count=signal.get('Count'),
                created_by=self.agent, updated_by=self.agent
            ) for signal in self.signals
        ]
        for signal in signalList:
            if not in_list_models(signal, signalqs):
                signalcreate.append(signal)
        for signal in signalqs:
            if not in_list_models(signal, signalList):
                signaldelete.append(signal.pk)
        if signalcreate:
            Signal.objects.bulk_create(signalcreate)
        if signaldelete:
            Signal.objects.filter(pk__in=signaldelete).delete()

    def update_dipendent_genuses(self, instance):
        samplecreate:list[Sample] = []
        sampledelete:list[int] = []
        sampleqs = Sample.objects.filter(planet=instance)
        sampleList = [
            Sample(
                planet=instance, type=SampleSignals.objects.get(eddn=sample.get('Genus')),
                created_by=self.agent, updated_by=self.agent
            ) for sample in self.genuses
        ]
        for sample in sampleList:
            if not in_list_models(sample, sampleqs):
                samplecreate.append(sample)
        for sample in sampleqs:
            if not in_list_models(sample, sampleList):
                sampledelete.append(sample.pk)
        if samplecreate:
            Sample.objects.bulk_create(samplecreate)
        if sampledelete:
            Sample.objects.filter(pk__in=sampledelete).delete()

    def update_dipendent(self, instance):
        self.update_dipendent_signals(instance)
        if self.genuses:
            self.update_dipendent_genuses(instance)

    def create_dipendent(self, instance):
        signalcreate = [
            Signal(
                planet=instance, type=SignalSignals.objects.get(eddn=signal.get('Type')), 
                count=signal.get('Count'),
                created_by=self.agent, updated_by=self.agent
            ) for signal in self.signals
        ]
        Signal.objects.bulk_create(signalcreate)
        if self.genuses:
            samplecreate = [
                Sample(
                    planet=instance, type=SampleSignals.objects.get(eddn=sample.get('Genus')),
                    created_by=self.agent, updated_by=self.agent
                ) for sample in self.genuses
            ]
            Sample.objects.bulk_create(samplecreate)

    def data_preparation(self, validated_data: dict) -> dict:
        super().data_preparation(validated_data)
        self.genuses = validated_data.get('Genuses', [])

    def update_or_create(self, validated_data: dict, *args, **kwargs):
        systemInstance, create = create_or_update_if_time(
            System, time=self.get_time(), 
            defaults=self.get_data_defaults(validated_data, self.set_data_defaults_system),
            defaults_create=self.get_data_defaults_create(), defaults_update=self.get_data_defaults_update(),
            name=validated_data.get('StarSystem')
        )
        return super().update_or_create(validated_data, system=systemInstance)

    class Meta:
        model = Planet
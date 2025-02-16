from ..baseSerializer import BaseSerializer
from rest_framework import serializers

from ed_exploration.models import SignalSignals, Signal

from core.utility import in_list_models

class SignalListSerializer(serializers.ListSerializer):

    def validate(self, attrs):
        count = len(attrs)
        if count < 1:
            raise serializers.ValidationError(f"too few hotspots: {count}")
        return super().validate(attrs)
    
    def _get_planet(self, validated_data):
        return validated_data[0].get('planet')
    
    def create(self, validated_data):
        planet = self._get_planet(validated_data)
        signal_add = []
        signal_delete = []
        signal_qs = list(Signal.objects.filter(planet=planet))
        signal_list = [Signal(**item) for item in validated_data]
        for signal in signal_list:
            if not in_list_models(signal, signal_qs):
                signal_add.append(signal)
        for signal in signal_qs:
            if not in_list_models(signal, signal_list):
                signal_delete.append(signal.pk)
        if signal_add:
            signal_list = Signal.objects.bulk_create(signal_add)
        if signal_delete:
            Signal.objects.filter(pk__in=signal_delete).delete()
        return signal_list
        

class SignalSerializers(BaseSerializer):
    Type = serializers.SlugRelatedField(
        queryset=SignalSignals.objects.all(),
        slug_field='eddn',
        source='type',
    )
    Count = serializers.IntegerField(
        min_value=0,
        source='count',
    )

    class Meta:
        list_serializer_class = SignalListSerializer
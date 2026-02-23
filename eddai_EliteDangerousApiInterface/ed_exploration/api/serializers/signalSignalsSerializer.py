from rest_framework import serializers

from ed_exploration.models import SignalSignals

class SignalSignalsSerializer(serializers.ModelSerializer):
    """
    SignalSignalsSerializer is a serializer for the SignalSignals model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """

    class Meta:
        model = SignalSignals
        fields = ['id', 'name']

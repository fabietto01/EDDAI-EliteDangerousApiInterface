from rest_framework import serializers

from ed_exploration.models import SampleSignals

class SampleSignalsSerializer(serializers.ModelSerializer):
    """
    SampleSignalsSerializer is a serializer for the SampleSignals model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """

    class Meta:
        model = SampleSignals
        fields = ['id', 'name']

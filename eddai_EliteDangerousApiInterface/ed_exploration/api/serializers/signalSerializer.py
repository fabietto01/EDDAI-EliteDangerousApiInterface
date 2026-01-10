from rest_framework import serializers

from ed_exploration.models import Signal, SignalSignals

class SignalSerializer(serializers.ModelSerializer):
    """
    SignalSerializer is a serializer for the Signal model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """

    type = serializers.SlugRelatedField(
        queryset=SignalSignals.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = Signal
        fields = None
        exclude = ['planet']
        read_only_fields = [
            'created_at', 'updated_at',
            'created_by', 'updated_by',
            'planet'
        ]

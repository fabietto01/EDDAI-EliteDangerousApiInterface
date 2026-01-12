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

    def validate(self, attrs):
        try:
            planet_pk:int = self.context['planet_pk']
            signal_pk:int = self.instance.pk if self.instance else None
            if Signal.objects.filter(planet_id=planet_pk, type=attrs['type']).exclude(id=signal_pk).exists():
                raise serializers.ValidationError('Signal with this type already exists in this planet.')
        except KeyError:
            from rest_framework import status
            raise serializers.ValidationError('An internal server error occurred', code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return attrs

    class Meta:
        model = Signal
        fields = None
        exclude = ['planet']
        read_only_fields = [
            'created_at', 'updated_at',
            'created_by', 'updated_by',
            'planet'
        ]

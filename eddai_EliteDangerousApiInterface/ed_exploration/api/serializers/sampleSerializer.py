from rest_framework import serializers

from ed_exploration.models import Sample, SampleSignals

class SampleSerializer(serializers.ModelSerializer):
    """
    SampleSerializer is a serializer for the Sample model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """

    type = serializers.SlugRelatedField(
        queryset=SampleSignals.objects.all(),
        slug_field='name'
    )

    def validate(self, attrs):
        try:
            planet_pk:int = self.context['planet_pk']
            sample_pk:int = self.instance.pk if self.instance else None
            if Sample.objects.filter(planet_id=planet_pk, type=attrs['type']).exclude(id=sample_pk).exists():
                raise serializers.ValidationError('Sample with this type already exists in this planet.')
        except KeyError:
            from rest_framework import status
            raise serializers.ValidationError('An internal server error occurred', code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return attrs

    class Meta:
        model = Sample
        fields = None
        exclude = ['planet']
        read_only_fields = [
            'created_at', 'updated_at',
            'created_by', 'updated_by',
            'planet'
        ]

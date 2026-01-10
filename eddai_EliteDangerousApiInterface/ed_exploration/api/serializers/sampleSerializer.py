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

    class Meta:
        model = Sample
        fields = None
        exclude = ['planet']
        read_only_fields = [
            'created_at', 'updated_at',
            'created_by', 'updated_by',
            'planet'
        ]

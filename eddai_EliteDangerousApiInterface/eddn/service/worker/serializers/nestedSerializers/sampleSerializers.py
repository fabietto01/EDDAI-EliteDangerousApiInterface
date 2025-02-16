from ..baseSerializer import BaseSerializer
from rest_framework import serializers

from ed_exploration.models import SampleSignals, Sample

from core.utility import in_list_models

class SampleListSerializer(serializers.ListSerializer):
    
    def _get_planet(self, validated_data):
        return validated_data[0].get('planet')
    
    def create(self, validated_data):
        planet = self._get_planet(validated_data)
        sample_add = []
        sample_delete = []
        sample_qs = list(Sample.objects.filter(planet=planet))
        sample_list = [Sample(**item) for item in validated_data]
        for sample in sample_list:
            if not in_list_models(sample, sample_qs):
                sample_add.append(sample)
        for sample in sample_qs:
            if not in_list_models(sample, sample_list):
                sample_delete.append(sample.pk)
        if sample_add:
            sample_list = Sample.objects.bulk_create(sample_add)
        if sample_delete:
            Sample.objects.filter(pk__in=sample_delete).delete()
        return sample_list

class SampleSerializers(BaseSerializer):
    Genus = serializers.SlugRelatedField(
        queryset=SampleSignals.objects.all(),
        slug_field='eddn',
        source='type',
    )

    class Meta:
        list_serializer_class = SampleListSerializer
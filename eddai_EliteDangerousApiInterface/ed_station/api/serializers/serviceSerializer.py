from rest_framework import serializers

from ed_station.models import Service

class CompactedServiceSerializer(serializers.ModelSerializer):

    class Meta:
        model = Service
        fields = ['id', 'name']

class ServiceSerializer(CompactedServiceSerializer):

    class Meta(CompactedServiceSerializer.Meta):
        fields = None
        exclude = ['_eddn']
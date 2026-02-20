from rest_framework import serializers
from ed_bgs.models import Power

class PowerBasicInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Power
        fields = ['id', 'name']

class PowerSerializer(PowerBasicInformationSerializer):
    class Meta(PowerBasicInformationSerializer.Meta):
        fields = '__all__'

from rest_framework import serializers
from ed_bgs.models import PowerInSystem

class PowerInSystemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PowerInSystem
        exclude = ['system']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
        }

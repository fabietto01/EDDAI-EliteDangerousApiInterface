from rest_framework import serializers
from ed_system.models import System

from ed_core.api.serializers.DistanceSerializer import DistanceSerializer

class SystemSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = System
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
        }
        fields = "__all__"

class SystemDistanceSerializer(SystemSerializer, DistanceSerializer):
    pass
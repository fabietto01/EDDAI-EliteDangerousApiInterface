from os import read
from rest_framework import serializers
from ed_system.models import System

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

class SystemDistanceSerializer(SystemSerializer):
    
    distance = serializers.SerializerMethodField(read_only=True)

    def get_distance(self, instance:System):
        """
        restutuiser il campo distanza calcolato nella querry
        """
        return instance.distance
    

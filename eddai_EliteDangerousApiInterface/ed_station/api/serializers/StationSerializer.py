from rest_framework import serializers
from ed_station.models import Station

class StationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Station
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
        }
        fields = "__all__"
from rest_framework import serializers
from django.db.models import Model

class DistanceSerializer(serializers.ModelSerializer):
        
        distance_st = serializers.SerializerMethodField(read_only=True)
    
        def get_distance_st(self, instance:Model):
            """
            restutuiser il campo distanza calcolato nella querry
            """
            return instance.distance_st
from rest_framework import serializers, status

from ed_station.models import Service

class ServiceModelSerializes(serializers.ModelSerializer):
    """
    serializer dedicato alla visualizaione di servizzi
    """
    class Meta:
        model = Service
        exclude = ['_eddn']

class NestedServiceModelSerializes(serializers.ModelSerializer):
    """
    serializer dedicato alla visualizaione di servizzi
    """
    class Meta:
        model = Service
        exclude = ['_eddn', "description"]
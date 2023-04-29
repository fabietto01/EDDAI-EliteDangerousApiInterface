from rest_framework import serializers, status

from ed_station.models import StationType

class StationTypeModelSerializes(serializers.ModelSerializer):
    """
    serializer dedicato alla visualizaione di tipi di stazioni
    """
    
    class Meta:
        model = StationType
        exclude = ['_eddn']
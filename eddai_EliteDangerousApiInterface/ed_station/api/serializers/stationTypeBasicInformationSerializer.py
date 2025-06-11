from rest_framework import serializers
from ed_station.models import StationType

class StationTypeBasicInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = StationType
        fields = ['id', 'name']

class StationTypeSerializer(StationTypeBasicInformationSerializer):
    """
    Serializer for StationType model to provide basic information.
    Inherits from StationTypeBasicInformationSerializer.
    """
    class Meta(StationTypeBasicInformationSerializer.Meta):
        model = StationType
        fields = None
        exclude = ['_eddn', "eddn"]
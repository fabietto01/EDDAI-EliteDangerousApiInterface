from rest_framework import serializers
from ed_station.models import StationType

class StationTypeBasicInformationSerializer(serializers.ModelSerializer):

    class Meta:
        model = StationType
        fields = ['id', 'name']
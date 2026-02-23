from rest_framework import serializers
from ed_bgs.models import State

class StateBasicInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = State
        fields = ['id', 'name']

class StateSerializer(StateBasicInformationSerializer):
    class Meta(StateBasicInformationSerializer.Meta):
        fields = None
        exclude = ['_eddn', 'eddn']

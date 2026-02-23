from rest_framework import serializers
from ed_bgs.models import PowerState

class PowerStateBasicInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PowerState
        fields = ['id', 'name']

class PowerStateSerializer(PowerStateBasicInformationSerializer):
    class Meta(PowerStateBasicInformationSerializer.Meta):
        fields = None
        exclude = ['_eddn', 'eddn']

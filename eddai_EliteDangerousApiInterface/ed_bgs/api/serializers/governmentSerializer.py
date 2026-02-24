from rest_framework import serializers
from ed_bgs.models import Government

class GovernmentBasicInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Government
        fields = ['id', 'name']

class GovernmentSerializer(GovernmentBasicInformationSerializer):
    class Meta(GovernmentBasicInformationSerializer.Meta):
        fields = None
        exclude = ['_eddn', 'eddn']

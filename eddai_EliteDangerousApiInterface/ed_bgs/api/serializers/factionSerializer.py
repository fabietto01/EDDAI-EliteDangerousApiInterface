from rest_framework import serializers
from ed_bgs.models import Faction

class FactionBasicInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Faction
        fields = ['id', 'name']

class FactionSerializer(FactionBasicInformationSerializer):
    class Meta(FactionBasicInformationSerializer.Meta):
        fields = None
        exclude = ['_eddn', 'eddn']

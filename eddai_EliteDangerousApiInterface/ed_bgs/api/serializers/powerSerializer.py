from rest_framework import serializers
from ed_bgs.models import Power, Faction
from ed_system.models import System

class PowerBasicInformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Power
        fields = ['id', 'name']

class PowerSerializer(PowerBasicInformationSerializer):

    headquarter =  serializers.SlugRelatedField(
        queryset=System.objects.all(),
        slug_field='name',
    )

    allegiance = serializers.SlugRelatedField(
        queryset=Faction.objects.all(),
        slug_field='name',
    )

    class Meta(PowerBasicInformationSerializer.Meta):
        fields = '__all__'

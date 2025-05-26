from rest_framework import serializers

from ed_bgs.models import MinorFaction

class MinorFactionBasicInformation(serializers.ModelSerializer):

    class Meta:
        model = MinorFaction
        fields = ['id', 'name']
from rest_framework import serializers
from ed_bgs.models import StateInMinorFaction

class StateInMinorFactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = StateInMinorFaction
        exclude = ['minorFaction']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
        }

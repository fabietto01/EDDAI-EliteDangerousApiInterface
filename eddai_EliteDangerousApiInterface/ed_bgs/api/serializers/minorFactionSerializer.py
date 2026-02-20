from rest_framework import serializers
from ed_bgs.models import MinorFaction

class MinorFactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MinorFaction
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
        }

from rest_framework import serializers

from ed_bgs.models import MinorFaction

class MinorFactionSerializer(serializers.Serializer):
    Name = serializers.CharField(
        min_length=1,
    )
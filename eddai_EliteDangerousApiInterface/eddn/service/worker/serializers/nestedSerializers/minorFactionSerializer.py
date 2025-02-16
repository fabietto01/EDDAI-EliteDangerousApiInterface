from rest_framework import serializers

class MinorFactionSerializer(serializers.Serializer):
    Name = serializers.CharField(
        min_length=1,
    )
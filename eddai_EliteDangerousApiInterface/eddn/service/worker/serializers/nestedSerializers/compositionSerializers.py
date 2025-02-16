from rest_framework import serializers

class CompositionSerializers(serializers.Serializer):
    Ice = serializers.FloatField(
        min_value=0,
        max_value=100,
    )
    Rock = serializers.FloatField(
        min_value=0,
        max_value=100,
    )
    Metal = serializers.FloatField(
        min_value=0,
        max_value=100,
    )
from rest_framework import serializers

from ed_economy.models import Economy

class EconomySerializer(serializers.Serializer):
    Name = serializers.SlugRelatedField(
        queryset=Economy.objects.all(),
        slug_field='eddn',
    )
    Proportion = serializers.FloatField(
        min_value=0,
        max_value=1.15,
    )
from rest_framework import serializers

from ..customFields import EconomyFieldForEconomyLowerSlugRelatedField

class EconomyLowerSerializer(serializers.Serializer):
    name = EconomyFieldForEconomyLowerSlugRelatedField(
        slug_field='eddn',
    )
    proportion = serializers.FloatField(
        min_value=0,
        max_value=2,
    )
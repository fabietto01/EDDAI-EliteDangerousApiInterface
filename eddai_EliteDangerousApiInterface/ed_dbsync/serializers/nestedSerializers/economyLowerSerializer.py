from rest_framework import serializers
from ed_economy.models import Economy

from ..customFields import EconomyFieldForEconomyLowerSlugRelatedField

class EconomyLowerSerializer(serializers.Serializer):
    name = EconomyFieldForEconomyLowerSlugRelatedField(
        slug_field='eddn',
    )
    proportion = serializers.FloatField(
        min_value=Economy.get_min_proportion(),
        max_value=Economy.get_max_proportion(),
    )
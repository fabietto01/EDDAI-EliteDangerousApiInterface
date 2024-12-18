from rest_framework import serializers

from ed_economy.models import Commodity

from core.api.fields import CacheSlugRelatedField

class CommoditySerializer(serializers.Serializer):
    name = CacheSlugRelatedField(
        queryset=Commodity.objects.all(),
        slug_field='eddn',
    )
    buyPrice = serializers.IntegerField(
        min_value=0,
    )
    stock = serializers.IntegerField(
        min_value=0,
    )
    stockBracket = serializers.IntegerField(
        min_value=0,
    )
    sellPrice = serializers.IntegerField(
        min_value=0,
    )
    demand = serializers.IntegerField(
        min_value=0,
    )
    demandBracket = serializers.IntegerField(
        min_value=0,
    )
    meanPrice = serializers.IntegerField(
        min_value=0,
    )
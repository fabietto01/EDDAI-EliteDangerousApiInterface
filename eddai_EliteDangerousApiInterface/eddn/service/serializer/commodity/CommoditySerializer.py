from rest_framework import serializers
from django.db import OperationalError, ProgrammingError

from ed_economy.models import Commodity

from core.utility import get_values_list_or_default
from core.api.fields import CacheChoiceField

class CommoditySerializer(serializers.Serializer):
    name = CacheChoiceField(
        fun_choices=lambda: get_values_list_or_default(Commodity, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
        cache_key=Commodity.get_cache_key("eddn", flat=True),
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
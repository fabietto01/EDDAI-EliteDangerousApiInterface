from rest_framework import serializers
from django.db import OperationalError, ProgrammingError
import uuid

from ed_economy.models import Economy

from core.utility import get_values_list_or_default
from core.api.fields import CacheChoiceField

class EconomieSerializer(serializers.Serializer):
    name = CacheChoiceField(
        fun_choices=lambda: get_values_list_or_default(Economy, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
        cache_key=Economy.get_cache_key(),
    )
    proportion = serializers.FloatField(
        min_value=0,
    )
    
    class Meta:
        model = Economy
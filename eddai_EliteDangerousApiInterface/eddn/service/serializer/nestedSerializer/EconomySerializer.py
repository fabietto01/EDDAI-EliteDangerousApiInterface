from rest_framework import serializers
from eddn.service.serializer.customFields.CustomChoiceField import CustomCacheChoiceField
from django.db import OperationalError, ProgrammingError

from core.utility import get_values_list_or_default
from ed_economy.models import Economy

class EconomySerializer(serializers.Serializer):
    Name = CustomCacheChoiceField(
        fun_choices=lambda: get_values_list_or_default(Economy, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
        cache_key=Economy.get_cache_key("eddn", flat=True),
    )
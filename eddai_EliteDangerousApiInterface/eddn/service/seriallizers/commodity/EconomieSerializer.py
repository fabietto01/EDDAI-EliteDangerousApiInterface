from rest_framework import serializers
from django.db import OperationalError, ProgrammingError

from ed_economy.models import Economy

from core.utility import get_values_list_or_default

class EconomieSerializer(serializers.BaseSerializer):
    name = serializers.ChoiceField(
        choices=get_values_list_or_default(Economy, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
    )
    proportion = serializers.FloatField(
        min_value=0,
    )
    
    class Meta:
        model = Economy
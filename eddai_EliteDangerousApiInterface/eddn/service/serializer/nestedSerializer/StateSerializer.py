from rest_framework import serializers
from django.db import OperationalError, ProgrammingError
import uuid

from core.utility import get_values_list_or_default
from core.api.fields import CacheChoiceField

from ed_bgs.models import State

class StateSerializer(serializers.Serializer):
    State = CacheChoiceField(
        fun_choices=lambda: get_values_list_or_default(State.objects.exclude(type=State.TypeChoices.HAPPINESS.value), [], (OperationalError, ProgrammingError), 'eddn', flat=True),
        cache_key=uuid.uuid4(),
    )
    Trend = None
from rest_framework import serializers
from django.db import OperationalError, ProgrammingError

from core.utility import get_values_list_or_default

from ed_bgs.models import State

class StateSerializer(serializers.Serializer):
    State = serializers.ChoiceField(
        choices=get_values_list_or_default(State.objects.exclude(type=State.TypeChoices.HAPPINESS.value), [], (OperationalError, ProgrammingError), 'eddn', flat=True),
    )
    Trend = None
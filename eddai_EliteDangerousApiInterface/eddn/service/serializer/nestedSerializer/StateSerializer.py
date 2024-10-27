from rest_framework import serializers
from django.db import OperationalError, ProgrammingError

from core.utility import get_values_list_or_default
from core.api.fields import CacheSlugRelatedField

from ed_bgs.models import State

class StateSerializer(serializers.Serializer):
    State = CacheSlugRelatedField(
        queryset=State.objects.exclude(type=State.TypeChoices.HAPPINESS.value),
        slug_field='eddn',
    )
    Trend = None
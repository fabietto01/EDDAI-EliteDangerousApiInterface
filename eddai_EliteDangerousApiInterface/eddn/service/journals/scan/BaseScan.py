from rest_framework import serializers
from eddn.service.journals.BaseJournal import BaseJournal

from core.utility import update_or_create_if_time, get_values_list_or_default, get_or_none
from django.db import OperationalError, ProgrammingError

class BaseScan(BaseJournal):
    
    
    BodyName = serializers.CharField(
        max_length=255,
    )
    DistanceFromArrivalLS = serializers.FloatField(
        min_value=0,
    )
from rest_framework import serializers
from django.db import OperationalError, ProgrammingError
from eddn.service.journals.SAASignalsFound.SAASignalsFoundSerializers import SAASignalsFoundSerializers

from core.utility import update_or_create_if_time, get_values_list_or_default, get_or_none

from ed_mining.models import HotspotSignals, HotSpot


class HotspotSerializers(serializers.Serializer):
    Type = serializers.ChoiceField(
        choices=get_values_list_or_default(HotspotSignals, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
    )
    Count = serializers.IntegerField(
        min_value=0,
    )

class SAASignalsFoundHotspotSerializers(SAASignalsFoundSerializers):
    Signals = HotspotSerializers()

    class Meta:
        model = HotSpot
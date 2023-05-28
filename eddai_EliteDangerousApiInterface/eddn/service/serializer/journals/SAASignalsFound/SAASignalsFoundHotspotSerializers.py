from rest_framework import serializers
from django.db import OperationalError, ProgrammingError
from eddn.service.serializer.journals.SAASignalsFound.SAASignalsFoundSerializers import SAASignalsFoundSerializers

from core.utility import  in_list_models, get_values_list_or_default, update_or_create_if_time

from ed_mining.models import HotspotSignals, HotSpot
from ed_body.models import Ring

from ed_body.models import BaseBody
from ed_system.models import System

import re

class HotspotSerializers(serializers.Serializer):
    Type = serializers.ChoiceField(
        choices=get_values_list_or_default(HotspotSignals, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
    )
    Count = serializers.IntegerField(
        min_value=0,
    )

class SAASignalsFoundHotspotSerializers(SAASignalsFoundSerializers):
    """
    serializers dedicated to the Hotspot signals
    """
    Signals = serializers.ListField(
        child=HotspotSerializers(),
        min_length=1
    )

    def set_data_defaults(self, validated_data: dict) -> dict:
        return {
            'body': self.bodyInstance,
        }

    def set_data_defaults_body(self, validated_data: dict) -> dict:
        return {
            'bodyID': validated_data.get('BodyID')
        }

    def update_dipendent(self, instance):
        hotspotcreate:list[HotSpot] = []
        hotspotdelete:list[HotSpot] = []
        hostspotqs = HotSpot.objects.filter(ring=instance)
        hostspotqsList = list(hostspotqs)
        hostspotList = [
            HotSpot(
                ring=instance, type=HotspotSignals.objects.get(eddn=hostspot.get('Type')), 
                count=hostspot.get('Count')
            ) for hostspot in self.signals
        ]
        for hostspot in hostspotList:
            if not in_list_models(hostspot, hostspotqsList, ['id','pk','updated']):
                hotspotcreate.append(hostspot)
        for hostspot in hostspotqsList:
            if not in_list_models(hostspot, hostspotList, ['id','pk','updated']):
                hotspotdelete.append(hostspot)
        if hotspotcreate:
            HotSpot.objects.bulk_create(hotspotcreate)
        if hotspotdelete:
            hostspotqs.filter(pk__in=[h.pk for h in hotspotdelete]).delete()
    
    def create_dipendent(self, instance):
        hostspotList = [
            HotSpot(
                ring=instance, type=HotspotSignals.objects.get(eddn=hostspot.get('Type')), 
                count=hostspot.get('Count')
            ) for hostspot in self.signals
        ]
        HotSpot.objects.bulk_create(hostspotList)
    
    def update_or_create(self, validated_data: dict, *args, **kwargs):
        self.systemInstance, create = update_or_create_if_time(
            System, time=self.get_time(),
            defaults=self.get_data_defaults(validated_data, self.set_data_defaults_system),
            name=validated_data.get('StarSystem'),
        )
        bodyName = re.sub(
            r"\s[A-Z]\sRing$", "", validated_data.get('BodyName'), 0, 
        )
        self.bodyInstance, created = update_or_create_if_time(
            BaseBody, time=self.get_time(), 
            defaults=self.get_data_defaults(validated_data, self.set_data_defaults_body),
            name=bodyName, system=self.systemInstance
        )
        return super().update_or_create(validated_data, body=self.bodyInstance)

    class Meta:
        model = Ring
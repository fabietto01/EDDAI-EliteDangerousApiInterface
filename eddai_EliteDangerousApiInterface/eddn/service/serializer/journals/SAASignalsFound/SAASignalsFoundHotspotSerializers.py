from rest_framework import serializers
from eddn.service.serializer.journals.SAASignalsFound.SAASignalsFoundSerializers import SAASignalsFoundSerializers

from core.utility import  in_list_models, create_or_update_if_time
from core.api.fields import CacheSlugRelatedField

from ed_mining.models import HotspotType, HotSpot, Ring

from ed_body.models import BaseBody
from ed_system.models import System
import re

class HotspotSerializers(serializers.Serializer):
    Type = CacheSlugRelatedField(
        queryset=HotspotType.objects.all(),
        slug_field='eddn',
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
        hotspotdelete:list[int] = []
        hostspotqs = HotSpot.objects.filter(ring=instance)
        hostspotList = [
            HotSpot(
                ring=instance, type=HotspotType.objects.get(eddn=hostspot.get('Type')), 
                count=hostspot.get('Count'),
                created_by=self.agent, updated_by=self.agent
            ) for hostspot in self.signals
        ]
        for hostspot in hostspotList:
            if not in_list_models(hostspot, hostspotqs):
                hotspotcreate.append(hostspot)
        for hostspot in hostspotqs:
            if not in_list_models(hostspot, hostspotList):
                hotspotdelete.append(hostspot.pk)
        if hotspotcreate:
            HotSpot.objects.bulk_create(hotspotcreate)
        if hotspotdelete:
            hostspotqs.filter(pk__in=hotspotdelete).delete()
    
    def create_dipendent(self, instance):
        hostspotList = [
            HotSpot(
                ring=instance, type=HotspotType.objects.get(eddn=hostspot.get('Type')), 
                count=hostspot.get('Count'),
                created_by=self.agent, updated_by=self.agent
            ) for hostspot in self.signals
        ]
        HotSpot.objects.bulk_create(hostspotList)
    
    def update_or_create(self, validated_data: dict, *args, **kwargs):
        self.systemInstance, create = create_or_update_if_time(
            System, time=self.get_time(),
            defaults=self.get_data_defaults(validated_data, self.set_data_defaults_system),
            defaults_create=self.get_data_defaults_create(), defaults_update=self.get_data_defaults_update(),
            name=validated_data.get('StarSystem'),
        )
        bodyName = re.sub(
            r"\s[A-Z]\sRing$", "", validated_data.get('BodyName'), 0, 
        )
        self.bodyInstance, created = create_or_update_if_time(
            BaseBody, time=self.get_time(), 
            defaults=self.get_data_defaults(validated_data, self.set_data_defaults_body),
            defaults_create=self.get_data_defaults_create(), defaults_update=self.get_data_defaults_update(),
            name=bodyName, system=self.systemInstance
        )
        return super().update_or_create(validated_data, body=self.bodyInstance)

    class Meta:
        model = Ring
from rest_framework import serializers
from django.db import OperationalError, ProgrammingError
from eddn.service.journals.SAASignalsFound.SAASignalsFoundSerializers import SAASignalsFoundSerializers

from core.utility import  in_list_models, get_values_list_or_default

from ed_mining.models import HotspotSignals, HotSpot
from ed_body.models import Ring

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

    def update_dipendence(self, instance):
        hotspotcreate:list[HotSpot] = []
        hotspotdelete:list[HotSpot] = []
        hotspotupdate:list[HotSpot] = []
        hostspotqs = HotSpot.objects.filter(ring=instance)
        hostspotqsList = list(hostspotqs)
        hostspotList = [
            HotSpot(
                ring=instance, type=HotspotSignals.objects.get(name=hostspot.get('Type')), 
                count=hostspot.get('Count')
            ) for hostspot in self.signals
        ]
        for hostspot in hostspotList:
            if in_list_models(hostspot, hostspotqsList, ['id','pk','updated','count']):
                conuntupdate:HotSpot = filter(lambda x: x.type.name == hostspot.type.name, hostspotqsList)[0]
                if conuntupdate.count != hostspot.count:
                    conuntupdate.count = hostspot.count
                    hotspotupdate.append(conuntupdate)
            else:
                hotspotcreate.append(hostspot)
        for hostspot in hostspotqsList:
            if not in_list_models(hostspot, hostspotList, ['id','pk','updated','count']):
                hotspotdelete.append(hostspot)
        if hotspotcreate:
            HotSpot.objects.bulk_create(hotspotcreate)
        if hotspotupdate:
            hostspotqs.bulk_update(hotspotupdate, ['count'])
        if hotspotdelete:
            hostspotqs.filter(pk__in=[h.id for h in hotspotdelete]).delete()
    
    def create_dipendence(self, instance):
        hostspotList = [
            HotSpot(
                ring=instance, type=HotspotSignals.objects.get(name=hostspot.get('Type')), 
                count=hostspot.get('Count')
            ) for hostspot in self.signals
        ]
        HotSpot.objects.bulk_create(hostspotList)

    class Meta:
        model = Ring
from ..baseSerializer import BaseSerializer
from rest_framework import serializers

from ed_mining.models import HotspotType, HotSpot

from core.utility import in_list_models


class HotspotListSerializer(serializers.ListSerializer):

    def validate(self, attrs):
        count = len(attrs)
        if count < 1:
            raise serializers.ValidationError(f"too few hotspots: {count}")
        return super().validate(attrs)
    
    def _get_ring(self):
        return self.context.get('ring')
    
    def create(self, validated_data):
        hotspot_add = []
        hotspot_delete = []
        hotspot_qs = list(HotSpot.objects.filter(ring=self._get_ring()))
        hotspot_list = [HotSpot(**item) for item in validated_data]
        for hotspot in hotspot_list:
            if not in_list_models(hotspot, hotspot_qs):
                hotspot_add.append(hotspot)
        for hotspot in hotspot_qs:
            if not in_list_models(hotspot, hotspot_list):
                hotspot_delete.append(hotspot.pk)
        if hotspot_add:
            hotspot_list = HotSpot.objects.bulk_create(hotspot_add)
        if hotspot_delete:
            HotSpot.objects.filter(pk__in=hotspot_delete).delete()
        return hotspot_list

class HotspotSerializers(BaseSerializer):
    Type = serializers.SlugRelatedField(
        queryset=HotspotType.objects.all(),
        slug_field='eddn',
        source='type',
    )
    Count = serializers.IntegerField(
        min_value=0,
        source='count',
    )

    class Meta:
        list_serializer_class = HotspotListSerializer
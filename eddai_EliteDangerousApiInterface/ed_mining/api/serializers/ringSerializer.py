from rest_framework import serializers
from ed_core.api.serializers.DistanceSerializer import DistanceSerializer

from ed_body.api.serializers.baseBodySerializer import BaseBodyBasicInformation
from ed_system.api.serializers import SystemBasicInformation
from ed_mining.api.serializers.hotSpotInRing import HotSpotInRingBasicInformation

from ed_mining.models import Ring 
from ed_body.models import BaseBody

class RingSerializer(serializers.ModelSerializer):
    """
    RingModelSerializer is a serializer for the Ring model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """

    system = SystemBasicInformation(
        read_only=True, source='body.system'
    )
    body = BaseBodyBasicInformation(read_only=True)
    body_id = serializers.PrimaryKeyRelatedField(
        queryset=BaseBody.objects.all(),
        write_only=True,
        source='body',
    )
    hotSpot = HotSpotInRingBasicInformation(
        many=True,
        read_only=True,
        source='ed_mining_hotspot_related'
    )

    class Meta:
        model = Ring
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
        }
        fields = "__all__"

class RingDistanceSerializer(RingSerializer, DistanceSerializer):
    class Meta(RingSerializer.Meta):
        pass
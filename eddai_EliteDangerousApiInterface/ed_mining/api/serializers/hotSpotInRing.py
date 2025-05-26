from rest_framework import serializers

from ed_mining.models import HotSpot, HotspotType

class HotSpotInRingBasicInformation(serializers.ModelSerializer):
    """
    Serializer for the HotSpot model.
    """

    type = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )
    type_id = serializers.PrimaryKeyRelatedField(
        queryset=HotspotType.objects.all(),
        write_only=True,
        source='type',
    )

    class Meta:
        model = HotSpot
        fields = ['type', 'type_id', 'count']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
        }

class HotSpotInRingSerializer(HotSpotInRingBasicInformation):

    class Meta(HotSpotInRingBasicInformation.Meta):
        fields = None
        exclude = ['ring']
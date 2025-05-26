from rest_framework import serializers

from ed_mining.models import HotspotType

class HotspotTypeModelSerializer(serializers.ModelSerializer):
    """
    HotspotTypeModelSerializer is a serializer for the HotspotType model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """

    class Meta:
        model = HotspotType
        fields = ['id', 'name']
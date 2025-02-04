from rest_framework import serializers

from ed_economy.models import Commodity

class CompactedCommoditySerializer(serializers.ModelSerializer):
    """
    CommoditySerializer is a serializer for the Commodity model.
    Attributes:
        Meta (type): The metadata class for the serializer.
    """

    class Meta:
        model = Commodity
        fields = ['id', 'name', 'meanPrice']

class CommoditySerializer(serializers.ModelSerializer):
    
    class Meta(CompactedCommoditySerializer.Meta):
        fields = None
        exclude = ['_eddn', 'eddn']
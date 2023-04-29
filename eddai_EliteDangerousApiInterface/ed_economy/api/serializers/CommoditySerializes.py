from rest_framework import serializers, status

from ed_economy.models import Commodity

class CommodityModelSerializes(serializers.ModelSerializer):
    """
    serializer dedicato alla visualizaione di tipi di stazioni
    """
    
    class Meta:
        model = Commodity
        exclude = ['_eddn']
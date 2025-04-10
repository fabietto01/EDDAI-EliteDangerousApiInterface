from rest_framework import serializers

from ed_economy.models import CommodityInStation, Commodity

class CommodityInStatioBasicInformation(serializers.ModelSerializer):

    commodity = serializers.SlugRelatedField(
        queryset=Commodity.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = CommodityInStation
        fields = ['commodity',]
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
        }    
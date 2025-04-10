from rest_framework import serializers
from rest_framework import status

from ed_economy.models import Commodity, CommodityInStation

class CommodityInStationListSerializer(serializers.ListSerializer):

    def validate(self, attrs):
        try:
            station_pk:int = self.context["station_pk"]
            queryset = CommodityInStation.objects.filter(station_id=station_pk) \
                                                  .filter(commodity__in=[item.commodity for item in attrs])
            if queryset.exists():
                existing_commodities = [item.commodity.name for item in queryset]
                raise serializers.ValidationError(
                    f"CommodityInStation with station {station_pk} already has the following commodities: {', '.join(existing_commodities)}.",
                    code=status.HTTP_400_BAD_REQUEST
                )
        except KeyError:
            raise serializers.ValidationError('An internal server error occurred', code=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return attrs
    
    def create(self, validated_data):
        commodityInStation = [CommodityInStation(**item) for item in validated_data]
        return CommodityInStation.objects.bulk_create(commodityInStation)

class CommodityInStationSerializer(serializers.ModelSerializer):

    commodity = serializers.SlugRelatedField(
        queryset=Commodity.objects.all(),
        slug_field='name'
    )

    class Meta:
        model = CommodityInStation
        exclude = ['station']
        extra_kwargs = {
            'created_at': {'read_only': True},
            'updated_at': {'read_only': True},
            'created_by': {'read_only': True},
            'updated_by': {'read_only': True},
        }
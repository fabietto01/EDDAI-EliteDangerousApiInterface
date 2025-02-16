from ..baseSerializer import BaseSerializer
from rest_framework import serializers

from ..customFields import SlugLowerRelatedField, CustomIntegerField

from ed_economy.models import Commodity, CommodityInStation

from core.utility import in_list_models

class CommodityListSerializer(serializers.ListSerializer):

    def _get_station(self, validated_data):
        return validated_data[0].get('station')
    
    def get_commodity_mean_prices(self, validated_data):
        commodity_mean_prices = []
        for item in validated_data:
            commodity = item.get('commodity')
            mean_price = item.pop('commodity__meanPrice')
            if commodity and mean_price is not None:
                commodity_mean_prices.append({
                    'commodity': commodity,
                    'meanPrice': mean_price
                })
        return commodity_mean_prices
    
    def update_commodity_mean_prices(self, commodity_mean_prices):
        commodity_update = []
        for item in commodity_mean_prices:
            commodity:Commodity = item.get('commodity')
            mean_price = item.get('meanPrice')
            if commodity and mean_price is not None:
                if commodity.meanPrice != mean_price:
                    commodity.meanPrice = mean_price
                    commodity_update.append(commodity)
        if commodity_update:
            Commodity.objects.bulk_update(commodity_update, ['meanPrice'])

    def create(self, validated_data):
        commodity_mean_prices = self.get_commodity_mean_prices(validated_data)
        self.update_commodity_mean_prices(commodity_mean_prices)
        commodity_in_station_add = []
        commodity_in_station_delete = []
        commodity_in_station_qs = list(CommodityInStation.objects.filter(station=self._get_station(validated_data)))
        commodity_in_station_list = [CommodityInStation(**item) for item in validated_data]
        for commodity_in_station in commodity_in_station_list:
            if not in_list_models(commodity_in_station, commodity_in_station_qs):
                commodity_in_station_add.append(commodity_in_station)
        for commodity_in_station in commodity_in_station_qs:
            if not in_list_models(commodity_in_station, commodity_in_station_list):
                commodity_in_station_delete.append(commodity_in_station.id)
        if commodity_in_station_delete:
            CommodityInStation.objects.filter(id__in=commodity_in_station_delete).delete()
        if commodity_in_station_add:
            commodity_in_station_list = CommodityInStation.objects.bulk_create(commodity_in_station_add)
        return commodity_in_station_list


class CommoditySerializer(BaseSerializer):
    name = SlugLowerRelatedField(
        queryset=Commodity.objects.all(),
        slug_field='eddn',
        source='commodity',
    )
    buyPrice = CustomIntegerField(
        min_value=0,
    )
    stock = CustomIntegerField(
        min_value=0,
        source='inStock',
    )
    stockBracket = CustomIntegerField(
        allow_null=True,
        min_value=0,
        default=0,
    )
    sellPrice = CustomIntegerField(
        min_value=0,
    )
    demand = CustomIntegerField(
        min_value=0,
    )
    demandBracket = CustomIntegerField(
        allow_null=True,
        min_value=0,
        default=0,
    )
    meanPrice = CustomIntegerField(
        min_value=0,
        source='commodity__meanPrice',
    )

    class Meta:
        list_serializer_class = CommodityListSerializer
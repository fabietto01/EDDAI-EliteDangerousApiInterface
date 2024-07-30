from django.core.cache import cache
from rest_framework import serializers
from eddn.service.serializer.BaseSerializer import BaseSerializer
from eddn.service.serializer.commodity.CommoditySerializer import CommoditySerializer
from eddn.service.serializer.commodity.EconomieSerializer import EconomieSerializer

import uuid

from ed_system.models import System
from ed_station.models import Station
from ed_economy.models import Economy, Commodity, CommodityInStation

from core.utility import create_or_update_if_time, in_list_models, get_or_none

class CommodityV3Serializer(BaseSerializer):
    """
    serializer dedicato alla lavorazione dei dati con scema commodityV3
    link dello scemma https://eddn.edcd.io/schemas/commodity-v3.0.json
    """
    systemName = serializers.CharField(
        min_length=1
    )
    stationName = serializers.CharField(
        min_length=1
    )
    commodities = serializers.ListField(
        child=CommoditySerializer(),
        min_length=1
    )
    economies  = serializers.ListField(
        child=EconomieSerializer(),
        min_length=1,
    )
    StationType = None
    timestamp = serializers.DateTimeField(
        input_formats=[
            "%Y-%m-%dT%H:%M:%SZ"
        ]
    )

    def validate_systemName(self, value:str):
        """
        controlla che il sistema esista nel database
        """
        if not System.objects.filter(name=value).exists():
            raise serializers.ValidationError('System not found')
        return value

    def set_data_defaults(self, validated_data: dict) -> dict:
        economies = sorted(
            validated_data.get('economies', [{}]),
            key=lambda economy: economy.get('proportion', 0),
        )
        return { 
            'primaryEconomy': get_or_none(Economy, eddn=economies[0].get('name', None)) if economies else None,
            'secondaryEconomy': get_or_none(Economy, eddn=economies[1].get('name', None)) if len(economies) == 2 else None,
        }
    
    def data_preparation(self, validated_data: dict) -> dict:
        self.commodities_data:list[dict] = validated_data.pop('commodities', [])

    def update_meanPrice(self):
        """
        aggiorna il valore del meanPrice per ogni commodity
        """

        def get_meanPrice(value:str) -> int:
            """
            ritorna il valore del meanPrice
            """
            for commodity in commodities:
                if commodity.get('name') == value:
                    return commodity.get('meanPrice')
            return None

        commodities = []
        commodities_name = []
        commodities_update = []
        for commodity in self.commodities_data:
            commodities_name.append(commodity.get('name'))
            commodities.append({ 'name':commodity.get('name'), 'meanPrice':commodity.get('meanPrice')})
        for commodity in Commodity.objects.all():
            if commodity.eddn in commodities_name and commodity.updated_at < self.get_time():
                commodity.meanPrice = get_meanPrice(commodity.eddn)
                commodity.updated_at = self.agent
                commodities_update.append(commodity)
        if commodities_update:
            Commodity.objects.bulk_update(commodities_update, ['meanPrice', 'updated_at'])

    def create_commoditiesInstance(self, instance:Station):
        """
        funzione chiamata alle creazione di una nuova stazione, crea le istanze di commodity che sono vendute
        al interno della stazione stessa con tutti i campi necessari
        """
        commodities = [
            CommodityInStation(
                station=instance,
                commodity=Commodity.objects.get(eddn=commodity.get('name')),
                buyPrice=commodity.get('buyPrice'),
                stock=commodity.get('stock'),
                stockBracket=commodity.get('stockBracket'),
                sellPrice=commodity.get('sellPrice'),
                demand=commodity.get('demand'),
                demandBracket=commodity.get('demandBracket'),
                created_by=self.agent, updated_by=self.agent
            ) for commodity in self.commodities_data
        ]
        if commodities:
            Economy.objects.bulk_create(commodities)

    def update_commoditiesInstance(self, instance:Station):
        """
        funzione chiamata all aggiornamento di una stazione gia esistente, controla e aggiorna le istanze di commodity
        che sono vendute al interno della stazione stessa con tutti i campi necessari
        """

        def get_instance(commodity:Commodity) -> CommodityInStation:
            """
            ritorna l'istanza di CommodityInStation, presente all interno dei datti ricevuti,
            che ha come commodity la commodity passata come parametro
            """
            for commodity in commoditiesList:
                if commodity.commodity == commodity:
                    return commodity
            return None

        commoditiesCreate:list[CommodityInStation] = []
        commoditiesUpdate:list[CommodityInStation] = []
        commoditiesDelete:list[CommodityInStation] = []
        commoditiesqs = CommodityInStation.objects.filter(station=instance)
        commoditiesList = [
            CommodityInStation(
                station=instance, commodity=Commodity.objects.get(eddn=commodity.get('name')),
                buyPrice=commodity.get('buyPrice'),
                inStock=commodity.get('stock'), stockBracket=commodity.get('stockBracket'),
                sellPrice=commodity.get('sellPrice'),
                demand=commodity.get('demand'),demandBracket=commodity.get('demandBracket'),
                created_by=self.agent, updated_by=self.agent
            ) for commodity in self.commodities_data
        ]
        for commodity in commoditiesList:
            if not in_list_models(commodity, commoditiesqs, fields_include=['commodity']):
                commoditiesCreate.append(commodity)                
        for commodity in commoditiesqs:
            if not in_list_models(commodity, commoditiesList, fields_include=['commodity']):
                commoditiesDelete.append(commodity.commodity)
            else:
                update_instanze = get_instance(commodity.commodity)
                if commodity.updated < self.get_time():
                    commodity.buyPrice = update_instanze.buyPrice
                    commodity.inStock = update_instanze.inStock
                    commodity.stockBracket = update_instanze.stockBracket
                    commodity.sellPrice = update_instanze.sellPrice
                    commodity.demand = update_instanze.demand
                    commodity.demandBracket = update_instanze.demandBracket
                    commoditiesUpdate.append(commodity)
        if commoditiesCreate:
            CommodityInStation.objects.bulk_create(commoditiesCreate)
        if commoditiesUpdate:
            CommodityInStation.objects.bulk_update(commoditiesUpdate, ['buyPrice', 'inStock', 'stockBracket', 'sellPrice', 'demand', 'demandBracket'])
        if commoditiesDelete:
            commoditiesqs.filter(commodity__in=commoditiesDelete).delete()

    def create_dipendent(self, instance):
        self.update_meanPrice()
        self.create_commoditiesInstance(instance)

    def update_dipendent(self, instance):
        self.update_meanPrice()
        self.update_commoditiesInstance(instance)

    def update_or_create(self, validated_data: dict):
        self.data_preparation(validated_data)
        system = System.objects.get(name=validated_data.get('systemName'))
        self.instance, create = create_or_update_if_time(
            Station, time=self.get_time(), defaults=self.get_data_defaults(validated_data),
            defaults_create=self.get_data_defaults_create(), defaults_update=self.get_data_defaults_update(),
            update_function=self.update_dipendent, create_function=self.create_dipendent,
            name=validated_data.get('stationName'), system=system
        )
        return self.instance
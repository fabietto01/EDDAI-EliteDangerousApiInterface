from rest_framework import serializers
from .BaseJournal import BaseJournal
from django.db import OperationalError, ProgrammingError

from ..customFields import LandingPadsChoiceField
from ..nestedSerializer import BaseMinorFactionSerializer, EconomySerializer

from ed_station.models import (
    Service, ServiceInStation, StationType,
    Station
)
from ed_economy.models import Economy
from ed_bgs.models import MinorFaction, MinorFactionInSystem
from ed_system.models import System

from core.utility import (
    update_or_create_if_time, in_list_models, 
    get_values_list_or_default, get_or_none
)

class DockedSerializer(BaseJournal):
    LandingPads = LandingPadsChoiceField(
        choices=[key for key in Station.LandingPadChoices.names],
    )
    StationName = serializers.CharField(
        min_length=1,
    )
    StationType = serializers.ChoiceField(
        choices=get_values_list_or_default(StationType, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
    )
    DistFromStarLS = serializers.FloatField(
        min_value=0,
    )
    StationServices = serializers.MultipleChoiceField(
        choices=get_values_list_or_default(Service, [], (OperationalError, ProgrammingError), 'eddn', flat=True)
    )
    StationEconomies = serializers.ListField(
        child=EconomySerializer(),
        min_length = 1,
        max_length = 2,
    )
    StationFaction = BaseMinorFactionSerializer()

    def validate(self, attrs:dict):
        economies = attrs.get('StationEconomies', [])
        faction_Name = attrs.get('StationFaction', {}).get('Name')
        system_Name = attrs.get('StarSystem')
        if len(economies) == 2:
            if economies[0].get('Name', '') == economies[1].get('Name', ''):
                raise serializers.ValidationError({'StationEconomies': 'Economies must be different'})
        if not MinorFactionInSystem.objects.filter(system__name=system_Name, minorFaction__name=faction_Name).exists():
            raise serializers.ValidationError({'StationFaction':{'Name':f'the minor faction {faction_Name} is not present in the system {system_Name}'}})
        return super().validate(attrs)

    def set_data_defaults(self, validated_data: dict) -> dict:
        economies = validated_data.pop('StationEconomies', [{}])
        return {
            'landingPad': validated_data.get('LandingPads'),
            'type': StationType.objects.get(eddn=validated_data.pop('StationType')),
            'distance': validated_data.get('DistFromStarLS'),
            'minorFaction': MinorFaction.objects.get(name=validated_data.pop('StationFaction', {}).get('Name')),
            'primaryEconomy': get_or_none(Economy, eddn=economies[0].pop('Name')) if economies else None,
            'secondaryEconomy': get_or_none(Economy, eddn=economies[1].pop('Name')) if len(economies) == 2 else None,
        }
    
    def set_data_defaults_system(self, validated_data: dict) -> dict:
        return super(DockedSerializer, self).set_data_defaults(validated_data)

    def data_preparation(self, validated_data: dict) -> dict:
        self.services_in_station = validated_data.get('StationServices')

    def create_dipendent(self, instance):
        if self.services_in_station:
            services = [
                ServiceInStation(
                    station=instance, service=Service.objects.get(eddn=service)
                ) for service in self.services_in_station
            ]
            ServiceInStation.objects.bulk_create(services)

    def update_dipendent(self, instance: Station):
        if self.services_in_station:
            servicecreate:list[ServiceInStation] = []
            servicedelete:list[ServiceInStation] = []
            serviceqs = ServiceInStation.objects.filter(station=instance)
            serviceqsList = list(serviceqs)
            serviceList = [
                ServiceInStation(
                    station=instance, service=Service.objects.get(eddn=service)
                ) for service in self.services_in_station
            ]
            for service in serviceList:
                if not in_list_models(service, serviceqsList, ['id','pk','updated','created']):
                    servicecreate.append(service)
            for service in serviceqsList:
                if not in_list_models(service, serviceList, ['id','pk','updated','created']):
                    servicedelete.append(service)
            if servicecreate:
                ServiceInStation.objects.bulk_create(servicecreate)
            if servicedelete:
                ServiceInStation.objects.filter(id__in=[s.id for s in servicedelete]).delete()

    def update_or_create(self, validated_data: dict):
        self.data_preparation(validated_data)
        system, created = update_or_create_if_time(
            System, time=self.get_time(),
            defaults=self.get_data_defaults(validated_data, self.set_data_defaults_system),
            name=validated_data.get('StarSystem')
        )
        self.initial, created = update_or_create_if_time(
            Station, time=self.get_time(), 
            defaults=self.get_data_defaults(validated_data),
            update_function=self.update_dipendent, create_function=self.create_dipendent,
            system=system, name=validated_data.get('StationName'),
        )
        return self.initial
    
    class Meta:
        model = Station
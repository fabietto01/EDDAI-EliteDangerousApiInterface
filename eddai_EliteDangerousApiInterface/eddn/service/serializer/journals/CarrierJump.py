from rest_framework import serializers
from django.db import OperationalError, ProgrammingError
import uuid

from .BaseJournal import BaseJournal

from ..customFields import CustomCacheChoiceField, CustomChoiceField
from ..nestedSerializer import BaseMinorFactionSerializer, EconomySerializer

from ed_station.models import StationType, Service, Station, ServiceInStation
from ed_bgs.models import MinorFaction
from ed_economy.models import Economy
from ed_system.models import System
from ed_body.models import Planet, Star

from core.utility import create_or_update_if_time, get_values_list_or_default, get_or_none, in_list_models
from core.api.fields import CacheChoiceField

class CarrierJumpSerializer(BaseJournal):
    """
    serializer dedicato alla lavorazione dei dati con schema journal e evento CarrierJump
    """
    #-------------------------------------------------------------------------------
    Body = serializers.CharField(
        max_length=255,
    )
    BodyID = serializers.IntegerField(
        min_value=0,
    )
    BodyType = serializers.ChoiceField(
        choices=[
            "Planet", "Star"
        ]
    )
    #-------------------------------------------------------------------------------
    SystemEconomy = CustomCacheChoiceField(
        fun_choices=lambda: get_values_list_or_default(Economy, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
        cache_key=uuid.uuid4(),
        required=False,
        allow_blank=True,
    )
    SystemSecondEconomy = CustomCacheChoiceField(
        fun_choices=lambda: get_values_list_or_default(Economy, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
        cache_key=uuid.uuid4(),
        required=False,
        allow_blank=True,
    )
    SystemSecurity = CustomChoiceField(
        choices=[sc.lower() for sc in System.SecurityChoices.names],
        required=False,
    ) 
    Population = serializers.IntegerField(
        min_value=0,
    )
    #-------------------------------------------------------------------------------
    Docked = serializers.BooleanField()
    StationName = serializers.CharField(
        min_length=1,
    )
    StationType = CacheChoiceField(
        fun_choices=lambda:get_values_list_or_default(StationType, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
        cache_key=uuid.uuid4(),
    )
    StationFaction = BaseMinorFactionSerializer()
    StationServices = serializers.ListField(
        child=CacheChoiceField(
            fun_choices=lambda:get_values_list_or_default(Service, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
            cache_key=uuid.uuid4(),
        )
    )
    StationEconomies = serializers.ListField(
        child=EconomySerializer(),
        min_length = 1,
        max_length = 2,
    )
    #-------------------------------------------------------------------------------

    def validate(self, attrs):
        if not attrs.get('Docked'):
            raise serializers.ValidationError(
                'Docked must be True'
            )
        if attrs.get('StationType') != 'FleetCarrier':
            raise serializers.ValidationError(
                'StationType must be FleetCarrier'
            )
        faction_Name = attrs.get('StationFaction', {}).get('Name')
        if faction_Name != 'FleetCarrier':
            raise serializers.ValidationError(
                'StationFaction must be FleetCarrier'
            )
        return super().validate(attrs)
    
    def set_data_defaults_system(self, validated_data: dict) -> dict:
        defaults = super().set_data_defaults(validated_data)
        defaults.update({
            "primaryEconomy": get_or_none(Economy, eddn=validated_data.get('SystemEconomy', None)),
            "secondaryEconomy": get_or_none(Economy, eddn=validated_data.get('SystemSecondEconomy', None)),
            "security":  System.SecurityChoices[
                validated_data.get('SystemSecurity', '').capitalize()
            ].value if validated_data.get('SystemSecurity', None) else None,
            "population": validated_data.get('Population', None),
        })
        return defaults
    
    def set_data_defaults(self, validated_data: dict) -> dict:
        economies = validated_data.pop('StationEconomies', [{}])
        return {
            'type': StationType.objects.get(eddn=validated_data.pop('StationType')),
            'minorFaction': MinorFaction.objects.get(name=validated_data.pop('StationFaction', {}).get('Name')),
            'primaryEconomy': get_or_none(Economy, eddn=economies[0].pop('Name')) if economies else None,
            'secondaryEconomy': get_or_none(Economy, eddn=economies[1].pop('Name')) if len(economies) == 2 else None,
        }
    
    def data_preparation(self, validated_data: dict) -> dict:
        self.services_in_station = validated_data.get('StationServices')

    def create_dipendent(self, instance):
        if self.services_in_station:
            services = [
                ServiceInStation(
                    station=instance, service=Service.objects.get(eddn=service),
                    created_by=self.agent, updated_by=self.agent
                ) for service in self.services_in_station
            ]
            ServiceInStation.objects.bulk_create(services)

    def update_dipendent(self, instance: Station):
        if self.services_in_station:
            servicecreate:list[ServiceInStation] = []
            servicedelete:list[ServiceInStation] = []
            serviceqs = ServiceInStation.objects.filter(station=instance)
            serviceList = [
                ServiceInStation(
                    station=instance, service=Service.objects.get(eddn=service),
                    created_by=self.agent, updated_by=self.agent
                ) for service in self.services_in_station
            ]
            for service in serviceList:
                if not in_list_models(service, serviceqs):
                    servicecreate.append(service)
            for service in serviceqs:
                if not in_list_models(service, serviceList):
                    servicedelete.append(service)
            if servicecreate:
                ServiceInStation.objects.bulk_create(servicecreate)
            if servicedelete:
                ServiceInStation.objects.filter(id__in=[s.id for s in servicedelete]).delete()
    
    def update_or_create(self, validated_data: dict, update_function=None, create_function=None) -> System:
        self.data_preparation(validated_data)
        system, create = create_or_update_if_time(
            System, time=self.get_time(), defaults=self.get_data_defaults(validated_data, self.set_data_defaults_system),
            defaults_create=self.get_data_defaults_create(), defaults_update=self.get_data_defaults_update(),
            name=validated_data.get('StarSystem'),
        )
        ModelClass = None
        if validated_data.get('BodyType') == 'Planet':
            ModelClass = Planet
        elif validated_data.get('BodyType') == 'Star':
            ModelClass = Star
        body, create = create_or_update_if_time(
            ModelClass, time=self.get_time(), defaults={},
            defaults_create=self.get_data_defaults_create(), defaults_update=self.get_data_defaults_update(),
            system=system, name=validated_data.get('Body'), bodyID=validated_data.get('BodyID')
        )
        self.instance, create = create_or_update_if_time(
            Station, time=self.get_time(), defaults=self.get_data_defaults(validated_data),
            defaults_create=self.get_data_defaults_create(), defaults_update=self.get_data_defaults_update(),
            update_function=self.update_dipendent, create_function=self.create_dipendent,
            system=system, name=validated_data.get('StationName'),
        )
        return self.instance
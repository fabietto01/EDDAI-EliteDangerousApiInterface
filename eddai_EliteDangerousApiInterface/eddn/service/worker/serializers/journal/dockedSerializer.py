from rest_framework import serializers
from .baseJournalSerializer import BaseJournalSerializer

from ..customFields import LandingPadsChoiceField
from ..nestedSerializers import EconomySerializer, MinorFactionSerializer

from ed_economy.models import Economy
from ed_station.models import (
    Service, StationType,
    Station, ServiceInStation
)

from ed_bgs.models import MinorFaction, MinorFactionInSystem
from core.utility import (
    create_or_update_if_time, in_list_models
)

class DockedSerializer(BaseJournalSerializer):
    LandingPads = LandingPadsChoiceField()
    StationName = serializers.CharField(
        min_length=1,
    )
    StationType = serializers.SlugRelatedField(
        queryset=StationType.objects.all(),
        slug_field='eddn',
    )
    DistFromStarLS = serializers.FloatField(
        min_value=0,
    )
    StationServices = serializers.SlugRelatedField(
        queryset=Service.objects.all(),
        slug_field='eddn',
        many=True,
    )
    StationEconomies = serializers.ListField(
        child=EconomySerializer(),
        min_length = 1,
        max_length = 2,
    )
    StationFaction = MinorFactionSerializer()

    def _get_station_minor_faction_name(self, data) -> str:
        """Retrieve the name of the minor faction from the data."""
        StationFaction:dict = data.get('StationFaction')
        return StationFaction.get('Name')
    
    def _sort_economies(self, StationEconomies:list[dict]) -> None:
        """Sort the station economies by their proportion in descending order."""
        StationEconomies.sort(key=lambda x: x.get('Proportion'), reverse=True)

    def _get_primary_economy(self, data) -> Economy:
        """Get the primary economy from the sorted list of station economies."""
        StationEconomies:list[dict] = data.get('StationEconomies')
        self._sort_economies(StationEconomies)
        return StationEconomies[0].get('Name')
    
    def _get_secondary_economy(self, data) -> Economy:
        """Get the secondary economy from the sorted list of station economies."""
        StationEconomies:list[dict] = data.get('StationEconomies')
        if len(StationEconomies) == 1:
            return Economy.objects.get(eddn='$economy_None;')
        self._sort_economies(StationEconomies)
        return StationEconomies[1].get('Name')
    
    def validate(self, attrs:dict):
        """Validate the attributes of the station, ensuring economies are different and the faction is present in the system."""
        economies = attrs.get('StationEconomies', [])
        faction_Name = self._get_station_minor_faction_name(attrs)
        system_Name = attrs.get('StarSystem')
        if len(economies) == 2:
            if  self._get_primary_economy(attrs) == self._get_secondary_economy(attrs):
                raise serializers.ValidationError({'StationEconomies': 'Economies must be different'})
        if not ( attrs.get('StationType').eddn == 'FleetCarrier' and faction_Name == 'FleetCarrier' ):
            if not MinorFactionInSystem.objects.filter(system__name=system_Name, minorFaction__name=faction_Name).exists():
                raise serializers.ValidationError({'StationFaction':{'Name':f'the minor faction {faction_Name} is not present in the system {system_Name}'}})
        return super().validate(attrs)
    
    def set_data_defaults_station(self, validated_data:dict) -> dict:
        """Set default values for the station data."""
        return {
            "landingPad": validated_data.get('LandingPads'),
            "system": validated_data.get('system'),
            "type": validated_data.get('StationType'),
            "distance": validated_data.get('DistFromStarLS'),
            'minorFaction': MinorFaction.objects.get(name=self._get_station_minor_faction_name(validated_data)),
            'primaryEconomy': self._get_primary_economy(validated_data),
            'secondaryEconomy': self._get_secondary_economy(validated_data),
        }
        
    def get_service_in_station_instace(self, station, service, validated_data):
        """Create a ServiceInStation instance with the provided data."""
        return ServiceInStation(
            station=station, service=service,
            updated_by=validated_data.get('updated_by'),
            created_by=validated_data.get('created_by'),
            updated_at=validated_data.get('updated_at'),
            created_at=validated_data.get('updated_at'),
        )
    
    def get_list_services_in_validated_data(self, instance, validated_data):
        """Get a list of ServiceInStation instances from the validated data."""
        ServiceInStation = validated_data.get('StationServices')
        ServiceInStation_add = []
        for service in ServiceInStation:
            ServiceInStation_add.append(
                self.get_service_in_station_instace(instance, service, validated_data)
            )
        return ServiceInStation_add
    
    def run_create_services_in_station(self, instance, validated_data):
        """Create services in the station based on the validated data."""
        ServiceInStation_add = self.get_list_services_in_validated_data(instance, validated_data)
        if ServiceInStation_add:
            ServiceInStation.objects.bulk_create(ServiceInStation_add)

    def run_update_services_in_station(self, instance, validated_data):
        """Update services in the station based on the validated data."""
        ServiceInStation_add = []
        ServiceInStation_delete = []
        ServiceInStation_qs = list(ServiceInStation.objects.filter(station=instance))
        ServiceInStation_list = self.get_list_services_in_validated_data(instance, validated_data)
        for service in ServiceInStation_list:
            if not in_list_models(service, ServiceInStation_qs):
                ServiceInStation_add.append(service)
        for service in ServiceInStation_qs:
            if not in_list_models(service, ServiceInStation_list):
                ServiceInStation_delete.append(service.id)
        if ServiceInStation_add:
            ServiceInStation.objects.bulk_create(ServiceInStation_add)
        if ServiceInStation_delete:
            ServiceInStation.objects.filter(id__in=ServiceInStation_delete).delete()

    def create_dipendent(self, instance, validated_data):
        """Create dependent services in the station."""
        self.run_create_services_in_station(instance, validated_data)
    
    def update_dipendent(self, instance, validated_data):
        """Update dependent services in the station."""
        self.run_update_services_in_station(instance, validated_data)

    def update_or_create(self, validated_data, update_function=None, create_function=None):
        """Update or create a station with the provided validated data."""
        system = super().update_or_create(validated_data, update_function, create_function)
        def_create_dipendent = lambda instance: self.create_dipendent(instance, validated_data)
        def_update_dipendent = lambda instance: self.update_dipendent(instance, validated_data)
        kwargs = {}
        if validated_data.get('StationType').eddn != 'FleetCarrier':
            kwargs = {'system':system}
        station, create = create_or_update_if_time(
            Station, time=self.get_time(),
            defaults=self.get_data_defaults(validated_data, self.set_data_defaults_station),
            defaults_create=self.get_data_defaults_create(validated_data),
            defaults_update=self.get_data_defaults_update(validated_data),
            update_function=def_update_dipendent,
            create_function=def_create_dipendent,
            name=validated_data.get('StationName'),
            **kwargs
        )
        return station
from rest_framework import serializers
from .baseJournalSerializer import BaseJournalSerializer

from ..customFields import SystemSecurityChoiceField
from ..nestedSerializers import MinorFactionInSystemSerializer, MinorFactionSerializer, EconomySerializer

from ed_economy.models import Economy
from ed_station.models import (
    Service, StationType,
    Station, ServiceInStation
)
from ed_body.models import Planet, Star

from ed_bgs.models import MinorFaction
from core.utility import (
    create_or_update_if_time, in_list_models
)

class CarrierJumpSerializer(BaseJournalSerializer):
    SystemEconomy = serializers.SlugRelatedField(
        queryset=Economy.objects.all(),
        slug_field='eddn',
        required=False,
        allow_null=True,
    )
    SystemSecondEconomy = serializers.SlugRelatedField(
        queryset=Economy.objects.all(),
        slug_field='eddn',
        required=False,
        allow_null=True,
    )
    SystemSecurity = SystemSecurityChoiceField(
        required=False,
    )
    Population = serializers.IntegerField(
        min_value=0,
    )
    Factions = MinorFactionInSystemSerializer(
        many=True, required=False,
    )
    SystemFaction = MinorFactionSerializer(
        required=False,
    )
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
    StationName = serializers.CharField(
        min_length=1,
        required=False,
    )
    StationType = serializers.SlugRelatedField(
        queryset=StationType.objects.all(),
        slug_field='eddn',
        required=False,
    )
    StationFaction = MinorFactionSerializer(
        required=False,
    )
    StationServices = serializers.SlugRelatedField(
        queryset=Service.objects.all(),
        slug_field='eddn',
        many=True,
        required=False,
    )
    StationEconomies = serializers.ListField(
        child=EconomySerializer(),
        min_length = 1,
        max_length = 2,
        required=False,
    )
    Docked = serializers.BooleanField()

    def _get_is_docked(self, data:dict) -> bool:
        """Return whether the carrier is docked."""
        return data.get('Docked', False)

    def _get_body_class(self, data:dict):
        """Return the class of the body"""
        return eval(data.get('BodyType'))
    
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

    def validate(self, attrs):
        if self._get_is_docked(attrs):
            if not attrs.get('StationName', None):
                raise serializers.ValidationError(
                    'StationName must be provided if Docked is True'
                )
            if not attrs.get('StationType', None):
                raise serializers.ValidationError(
                    'StationType must be provided if Docked is True'
                )
            if not attrs.get('StationFaction', None):
                raise serializers.ValidationError(
                    'StationFaction must be provided if Docked is True'
                )
            if not attrs.get('StationServices', None):
                raise serializers.ValidationError(
                    'StationServices must be provided if Docked is True'
                )
            if not attrs.get('StationEconomies', None):
                raise serializers.ValidationError(
                    'StationEconomies must be provided if Docked is True'
                )
        return super().validate(attrs)

    def set_data_defaults(self, validated_data):
        """
        Sets default values for the validated data.
        This method updates the validated data with default values for 
        'primaryEconomy', 'secondaryEconomy', 'security', and 'population' 
        based on the provided validated data.
        Args:
            validated_data (dict): The validated data dictionary.
        Returns:
            dict: The updated dictionary with default values set.
        """
        defaults = super().set_data_defaults(validated_data)
        defaults.update(
            {
                "primaryEconomy": validated_data.get('SystemEconomy', None),
                "secondaryEconomy": validated_data.get('SystemSecondEconomy', None),
                "security":  validated_data.get('SystemSecurity', None),
                "population": validated_data.get('Population', None),
            }
        )
        return defaults
    
    def set_data_defaults_station(self, validated_data:dict) -> dict:
        return {
            "type":validated_data.get('StationType'),
            "primaryEconomy": self._get_primary_economy(validated_data),
            "secondaryEconomy": self._get_secondary_economy(validated_data),
            "minorFaction": MinorFaction.objects.get(name=self._get_station_minor_faction_name(validated_data)),
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
    
    def run_save_minor_factions(self, instance, validated_data):
        """
        Saves minor factions in the system.
        This method iterates over the 'Factions' data and saves each minor faction
        in the system using the MinorFactionInSystemSerializer.
        Args:
            instance: The system instance.
            validated_data (dict): The validated data dictionary.
        """
        for faction in self.initial_data.get('Factions', []):
            serializers = MinorFactionInSystemSerializer(data=faction)
            serializers.is_valid(raise_exception=True)
            serializers.save(
                created_by=validated_data.get('created_by'),
                updated_by=validated_data.get('updated_by'),
                updated_at=validated_data.get('updated_at'),
                system=instance,
            )
    
    def run_check_control_faction(self, instance, validated_data):
        """
        Checks and updates the controlling faction of the system.
        This method checks if the controlling faction has changed and updates the
        system instance accordingly.
        Args:
            instance: The system instance.
            validated_data (dict): The validated data dictionary.
        """
        var_SystemFaction:dict = validated_data.get('SystemFaction', None)
        if var_SystemFaction:
            conrollingFaction = MinorFaction.objects.get(name=var_SystemFaction.get('Name'))
            if not instance.conrollingFaction == conrollingFaction:
                instance.conrollingFaction = conrollingFaction
                instance.updated_by = validated_data.get('updated_by')
                instance.updated_at = validated_data.get('updated_at')
                instance.save(force_update=['conrollingFaction', 'updated_by', 'updated_at'])

    def create_dipendent(self, instance, validated_data:dict):
        self.run_save_minor_factions(instance, validated_data)
        self.run_check_control_faction(instance, validated_data)

    def update_dipendent(self, instance, validated_data:dict):
        self.run_save_minor_factions(instance, validated_data)
        self.run_check_control_faction(instance, validated_data)

    def create_dipendent_station(self, instance, validated_data:dict):
        """Create dependent services in the station."""
        self.run_create_services_in_station(instance, validated_data)

    def update_dipendent_station(self, instance, validated_data:dict):
        """Update dependent services in the station."""
        self.run_update_services_in_station(instance, validated_data)
    
    def update_or_create(self, validated_data):
        """
        Update or create the journal instance with the provided validated data.
        This method updates the journal instance with the provided validated data
        and creates a new instance if it does not exist.
        Args:
            validated_data (dict): The validated data dictionary.
        Returns:
            Journal: The updated or created journal instance.
        """
        def_create_dipendent = lambda instance: self.create_dipendent(instance, validated_data)
        def_update_dipendent = lambda instance: self.update_dipendent(instance, validated_data)
        system =  super().update_or_create(validated_data, def_update_dipendent, def_create_dipendent)
        body, create = create_or_update_if_time(
            self._get_body_class(validated_data), time=self.get_time(),
            defaults={}, defaults_create=self.get_data_defaults_create(validated_data),
            defaults_update=self.get_data_defaults_update(validated_data),
            system=system, name=validated_data.get('Body'), bodyID=validated_data.get('BodyID')
        )
        if self._get_is_docked(validated_data):
            def_create_dipendent_station = lambda instance: self.create_dipendent_station(instance, validated_data)
            def_update_dipendent_station = lambda instance: self.update_dipendent_station(instance, validated_data)
            station, create = create_or_update_if_time(
                Station, time=self.get_time(), 
                defaults=self.get_data_defaults(validated_data, self.set_data_defaults_station),
                defaults_create=self.get_data_defaults_create(validated_data), defaults_update=self.get_data_defaults_update(validated_data),
                update_function=def_update_dipendent_station, create_function=def_create_dipendent_station,
                system=system, name=validated_data.get('StationName'),
            )
        return system
from .baseJournalSerializer import BaseJournalSerializer
from rest_framework import serializers

from ..customFields import SystemSecurityChoiceField
from ..nestedSerializers import MinorFactionInSystemSerializer, MinorFactionSerializer, EconomySerializer

from ed_station.models import StationType, Station, Service, ServiceInStation
from ed_economy.models import Economy
from ed_bgs.models import Power, PowerState, PowerInSystem, MinorFaction
from ed_body.models import Planet, Star

from core.utility import create_or_update_if_time, in_list_models

class LocationSerializer(BaseJournalSerializer):
    """
    LocationSerializer is a particularly complex serializer that handles the serialization and validation of data related to a system, body, and station in the Elite Dangerous game.
    The serializer processes the following information in sequence:
    1. System information: This includes fields such as Population, SystemEconomy, SystemSecondEconomy, SystemSecurity, SystemFaction, Factions, Powers, and PowerplayState.
    2. Body information: This includes fields such as Body, BodyID, and BodyType. If the body is a station, the station-related information is ignored at this stage.
    3. Station information: This includes fields such as StationName, StationType, and StationServices. These fields are required if the body type is a station or if the Docked field is True.
    The last three fields, DistFromStarLS, Docked, and StationServices, are common and can be applicable to both body and station information.
    """
    Population = serializers.IntegerField(
        min_value=0,
    )
    SystemEconomy = serializers.SlugRelatedField(
        queryset=Economy.objects.all(),
        slug_field='eddn',
    )
    SystemSecondEconomy = serializers.SlugRelatedField(
        queryset=Economy.objects.all(),
        slug_field='eddn',
        required=False,
        allow_null=True,
    )
    SystemSecurity = SystemSecurityChoiceField()
    SystemFaction = MinorFactionSerializer(
        required=False,
    )
    Factions = MinorFactionInSystemSerializer(
        many=True, required=False,
    )
    Powers = serializers.ListField(
        child=serializers.SlugRelatedField(
            queryset=Power.objects.all(),
            slug_field='name'
        ),
        required=False,
        min_length=0,
        max_length=PowerInSystem.get_max_relations(),
    )
    PowerplayState = serializers.SlugRelatedField(
        queryset=PowerState.objects.all(),
        slug_field='eddn',
        required=False,
    )
    Body = serializers.CharField(
        min_length=1,
        max_length=255,
    )
    BodyID = serializers.IntegerField(
        min_value=0,
    )
    BodyType = serializers.ChoiceField(
        choices=[
            "Planet", "Star", "Station"
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
    StationFaction = MinorFactionSerializer(
        required=False,
    )
    DistFromStarLS = serializers.FloatField(
        min_value=0,
        required=False,
    )
    Docked = serializers.BooleanField()

    def _get_class_body_type(self, validated_data:dict) -> str:
        """
        Returns the class of the body
        """
        return eval(validated_data.get('BodyType'))
    
    def _get_is_doced(self, validated_data:dict) -> bool:
        """
        Returns the value of the Docked field
        """
        return validated_data.get('Docked')
    
    def _get_station_minor_faction_name(self, data) -> str:
        """Retrieve the name of the minor faction from the data."""
        StationFaction:dict = data.get('StationFaction')
        return StationFaction.get('Name')
    
    def _sort_economies(self, StationEconomies:list[dict]) -> None:
        """Sort the station economies by their proportion in descending order."""
        StationEconomies.sort(key=lambda x: x.get('Proportion'), reverse=True)

    def _get_station_primary_economy(self, data) -> Economy:
        """Get the primary economy from the sorted list of station economies."""
        StationEconomies:list[dict] = data.get('StationEconomies')
        self._sort_economies(StationEconomies)
        return StationEconomies[0].get('Name')
    
    def _get_station_secondary_economy(self, data) -> Economy:
        """Get the secondary economy from the sorted list of station economies."""
        StationEconomies:list[dict] = data.get('StationEconomies')
        if len(StationEconomies) == 1:
            return Economy.objects.get(eddn='$economy_None;')
        self._sort_economies(StationEconomies)
        return StationEconomies[1].get('Name')
    
    def _get_factions_name(self, data) -> list[str]:
        """Retrieve the names of the minor factions from the data."""
        return [faction.get('Name') for faction in data.get('Factions', [])]

    def validate(self, attrs:dict):
        """
        controlla se Docked è True e in tal caso controlla che StationName e StationType siano presenti
        """ 
        if self._get_class_body_type(attrs) == Station and not self._get_is_doced(attrs):
            raise serializers.ValidationError({'Docked': 'This field is required when BodyType is Station'})
        if self._get_is_doced(attrs) or self._get_class_body_type(attrs) == Station:
            if not attrs.get('StationName', None):
                raise serializers.ValidationError({'StationName': 'This field is required when Docked is True'})
            if not attrs.get('StationType', None):
                raise serializers.ValidationError({'StationType': 'This field is required when Docked is True'})
            if not attrs.get('StationServices', None):
                raise serializers.ValidationError({'StationServices': 'This field is required when Docked is True'})
            if not attrs.get('StationEconomies', None):
                raise serializers.ValidationError({'StationEconomies': 'This field is required when Docked is True'})
            if not attrs.get('StationFaction', None):
                raise serializers.ValidationError({'StationFaction': 'This field is required when Docked is True'})
            economies = attrs.get('StationEconomies', [])
            if len(economies) == 2:
                if self._get_station_primary_economy(attrs) == self._get_station_secondary_economy(attrs):
                    raise serializers.ValidationError({'StationEconomies': 'The primary and secondary economies must be different'})
            if not ( attrs.get('StationType').eddn == 'FleetCarrier' and self._get_station_minor_faction_name(attrs) == 'FleetCarrier' ):
                if not self._get_station_minor_faction_name(attrs) in self._get_factions_name(attrs):
                    raise serializers.ValidationError({'StationFaction':{'Name':f'the minor faction {self._get_station_minor_faction_name(attrs)} is not present in the system {attrs.get("StarSystem")}'}})
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
    
    def set_data_defaults_body(self, validated_data: dict) -> dict:
        return {
            'distance': validated_data.get('DistFromStarLS', None),
        }
    
    def set_data_defaults_stastion(self, validated_data: dict) -> dict:
        return {
            'type': validated_data.get('StationType', None),
            "distance": validated_data.get('DistFromStarLS'),
            'minorFaction': MinorFaction.objects.get(name=self._get_station_minor_faction_name(validated_data)),
            'primaryEconomy': self._get_station_primary_economy(validated_data),
            'secondaryEconomy': self._get_station_secondary_economy(validated_data),
        }                                
    
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

    def get_powers_in_system_instace(self, system, power, state, validated_data):
        """
        Creates a PowerInSystem instance.
        This method creates and returns a PowerInSystem instance based on the provided
        system, power, state, and validated data.
        Args:
            system: The system instance.
            power: The power instance.
            state: The power state instance.
            validated_data (dict): The validated data dictionary.
        Returns:
            PowerInSystem: The created PowerInSystem instance.
        """
        return PowerInSystem(
            system=system,
            power=power,
            state=state,
            updated_by=validated_data.get('updated_by'),
            created_by=validated_data.get('created_by'),
            updated_at=validated_data.get('updated_at'),
            created_at=validated_data.get('updated_at'),
        )

    def get_list_powers_in_system_in_validated_data(self, instance, validated_data):
        """
        Gets a list of PowerInSystem instances from validated data.
        This method creates and returns a list of PowerInSystem instances based on the
        provided validated data.
        Args:
            instance: The system instance.
            validated_data (dict): The validated data dictionary.
        Returns:
            list: A list of PowerInSystem instances.
        """
        powers = validated_data.get('Powers', [])
        power_add = []
        for power in powers:
            power_add.append(
                self.get_powers_in_system_instace(
                    instance, power, validated_data.get('PowerplayState'), validated_data
                )
            )
        return power_add

    def run_create_powers_in_system(self, instance, validated_data):
        """
        Creates PowerInSystem instances.
        This method creates PowerInSystem instances based on the validated data and
        associates them with the system instance.
        Args:
            instance: The system instance.
            validated_data (dict): The validated data dictionary.
        """
        power_add = self.get_list_powers_in_system_in_validated_data(instance, validated_data)
        if power_add:
            PowerInSystem.objects.bulk_create(power_add)

    def run_update_powers_in_system(self, instance, validated_data):
        """
        Updates PowerInSystem instances.
        This method updates the PowerInSystem instances associated with the system
        instance based on the validated data.
        Args:
            instance: The system instance.
            validated_data (dict): The validated data dictionary.
        """
        power_add = []
        power_delete = []
        power_qs_list = list(PowerInSystem.objects.filter(system=instance))
        power_list = self.get_list_powers_in_system_in_validated_data(instance, validated_data)
        for power in power_list:
            if not in_list_models(power, power_qs_list):
                power_add.append(power)
        for power in power_qs_list:
            if not in_list_models(power, power_list):
                power_delete.append(power.id)
        if power_delete:
            PowerInSystem.objects.filter(id__in=power_delete).delete()
        if power_add:
            PowerInSystem.objects.bulk_create(power_add)

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

    def create_dipendent(self, instance, validated_data:dict):
        self.run_save_minor_factions(instance, validated_data)
        self.run_check_control_faction(instance, validated_data)
        self.run_create_powers_in_system(instance, validated_data)

    def update_dipendent(self, instance, validated_data:dict):
        self.run_save_minor_factions(instance, validated_data)
        self.run_check_control_faction(instance, validated_data)
        self.run_update_powers_in_system(instance, validated_data)

    def create_station_dipendent(self, instance, validated_data):
        """Create dependent services in the station."""
        self.run_create_services_in_station(instance, validated_data)

    def update_station_dipendent(self, instance, validated_data):
        """Update dependent services in the station."""
        self.run_update_services_in_station(instance, validated_data)

    def update_or_create(self, validated_data, update_function=None, create_function=None):
        def_create_dipendent = lambda instance: self.create_dipendent(instance, validated_data)
        def_update_dipendent = lambda instance: self.update_dipendent(instance, validated_data)
        system =  super().update_or_create(validated_data, def_update_dipendent, def_create_dipendent)
        class_body_type = self._get_class_body_type(validated_data)
        if class_body_type != Station:
            create_or_update_if_time(
                class_body_type, self.get_time(),
                defaults=self.get_data_defaults(validated_data, self.set_data_defaults_body),
                defaults_update=self.get_data_defaults_update(validated_data),
                defaults_create=self.get_data_defaults_create(validated_data),
                system=system, name=validated_data.get('Body'), bodyID=validated_data.get('BodyID'),
            )
        if self._get_is_doced(validated_data):
            def_create_station_dipendent = lambda instance: self.create_station_dipendent(instance, validated_data)
            def_update_station_dipendent = lambda instance: self.update_station_dipendent(instance, validated_data)
            create_or_update_if_time(
                Station, self.get_time(),
                defaults=self.get_data_defaults(validated_data, self.set_data_defaults_stastion),
                defaults_update=self.get_data_defaults_update(validated_data),
                defaults_create=self.get_data_defaults_create(validated_data),
                update_function=def_update_station_dipendent,
                create_function=def_create_station_dipendent,
                system=system, name=validated_data.get('StationName')
            )
        return system
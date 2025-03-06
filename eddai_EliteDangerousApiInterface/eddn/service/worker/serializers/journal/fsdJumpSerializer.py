from .baseJournalSerializer import BaseJournalSerializer
from rest_framework import serializers

from ..customFields import SystemSecurityChoiceField
from ..nestedSerializers import MinorFactionInSystemSerializer, MinorFactionSerializer

from ed_economy.models import Economy
from ed_bgs.models import Power, PowerState, PowerInSystem, MinorFaction
from ed_system.models import System

from core.utility import in_list_models

class FSDJumpSerializer(BaseJournalSerializer):
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

    def create_dipendent(self, instance, validated_data):
        """
        Creates dependent data for the system.
        This method creates minor factions and PowerInSystem instances for the system
        instance based on the validated data.
        Args:
            instance: The system instance.
            validated_data (dict): The validated data dictionary.
        """
        self.run_save_minor_factions(instance, validated_data)
        self.run_check_control_faction(instance, validated_data)
        self.run_create_powers_in_system(instance, validated_data)

    def update_dipendent(self, instance, validated_data):
        """
        Updates dependent data for the system.
        This method updates minor factions and PowerInSystem instances for the system
        instance based on the validated data.
        Args:
            instance: The system instance.
            validated_data (dict): The validated data dictionary.
        """
        self.run_save_minor_factions(instance, validated_data)
        self.run_check_control_faction(instance, validated_data)
        self.run_update_powers_in_system(instance, validated_data)

    def update_or_create(self, validated_data: dict) -> System:
        """
        Updates or creates a system instance.
        This method updates or creates a system instance based on the validated data
        and handles the creation or update of dependent data.
        Args:
            validated_data (dict): The validated data dictionary.
        Returns:
            System: The updated or created system instance.
        """
        def_create_dipendent = lambda instance: self.create_dipendent(instance, validated_data)
        def_update_dipendent = lambda instance: self.update_dipendent(instance, validated_data)
        return super().update_or_create(validated_data, def_update_dipendent, def_create_dipendent)
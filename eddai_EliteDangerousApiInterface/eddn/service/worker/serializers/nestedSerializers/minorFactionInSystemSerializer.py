from ..baseSerializer import BaseSerializer
from rest_framework import serializers

from .stateSerializer import StateSerializer

from core.utility import (
    create_or_update_if_time, in_list_models, 
)

from ed_bgs.models import (
    Faction, Government, State, MinorFactionInSystem, 
    MinorFaction, StateInMinorFaction
)

class MinorFactionInSystemListSerializer(serializers.ListSerializer):

    def validate(self, attrs):
        count = len(attrs)
        if count > MinorFactionInSystem.get_max_relations():
            raise serializers.ValidationError(f"too many factions: {count}")
        if count < 1:
            raise serializers.ValidationError(f"too few factions: {count}")
        return super().validate(attrs)

class MinorFactionInSystemSerializer(BaseSerializer):
    Name = serializers.CharField(
        min_length=1,
    )
    Allegiance = serializers.SlugRelatedField(
        queryset=Faction.objects.all(),
        slug_field='eddn',
    )
    Government = serializers.SlugRelatedField(
        queryset=Government.objects.all(),
        slug_field='eddn',
    )
    Influence = serializers.FloatField(
        min_value=0, max_value=1,
    )
    Happiness = serializers.SlugRelatedField(
        queryset=State.objects.filter(type=State.TypeChoices.HAPPINESS.value),
        slug_field='eddn',
        required = False,
        allow_null=True,
    )
    RecoveringStates = StateSerializer(
        many=True,
        required = False,
    )
    ActiveStates = StateSerializer(
        many=True,
        required = False,
    )
    PendingStates = StateSerializer(
        many=True,
        required = False,
    )

    def set_data_defaults(self, validated_data):
        return {
            "allegiance": validated_data.get('Allegiance'),
            "government": validated_data.get('Government'),
        }

    def set_data_defaults_create(self, validated_data):
        return {
            "created_by": validated_data.get('created_by'),
            "updated_by": validated_data.get('updated_by'),
            "updated_at": validated_data.get('updated_at'),
            "created_at": validated_data.get('updated_at'),
        }

    def set_data_defaults_update(self, validated_data):
        return {
            "updated_by": validated_data.get('updated_by'),
            "updated_at": validated_data.get('updated_at'),
        }
    
    def set_data_defaults_MinorFactionInSystem(self, validated_data):
        return {
            "Influence": validated_data.get('Influence'),
        }
    
    def get_state_instace(self, minorFactionInSystem, state, phase, validated_data):
        return StateInMinorFaction(
            minorFaction=minorFactionInSystem,
            state=state,
            phase=phase,
            updated_by=validated_data.get('updated_by'),
            created_by=validated_data.get('created_by'),
            updated_at=validated_data.get('updated_at'),
            created_at=validated_data.get('updated_at'),
        )
    
    def get_list_status_in_validated_data(self, instance, validated_data):
        status_add = []
        happiness = validated_data.get('Happiness', None)
        if happiness:
            status_add.append(
                self.get_state_instace(
                    instance, happiness, StateInMinorFaction.PhaseChoices.ACTIVE.value, validated_data
                )
            )
        for data in validated_data.get('RecoveringStates', []):
            status_add.append(
                self.get_state_instace(
                    instance, data.get('State'), StateInMinorFaction.PhaseChoices.RECOVERING.value, validated_data 
                )
            )
        for data in validated_data.get('ActiveStates', []):
            status_add.append(
                self.get_state_instace(
                    instance, data.get('State'), StateInMinorFaction.PhaseChoices.ACTIVE.value, validated_data
                )
            )
        for data in validated_data.get('PendingStates', []):
            status_add.append(
                self.get_state_instace(
                    instance, data.get('State'), StateInMinorFaction.PhaseChoices.PENDING.value, validated_data
                )
            )
        return status_add
    
    def create_state(self, instance, validated_data):
        status_add = self.get_list_status_in_validated_data(instance, validated_data)
        if status_add:
            StateInMinorFaction.objects.bulk_create(status_add)

    def update_state(self, instance, validated_data):
        state_add = []
        state_delete = []
        state_qs_list = list(StateInMinorFaction.objects.filter(minorFaction=instance))
        state_list = self.get_list_status_in_validated_data(instance, validated_data)
        for state in state_list:
            if not in_list_models(state, state_qs_list):
                state_add.append(state)
        for state in state_qs_list:
            if not in_list_models(state, state_list, ):
                state_delete.append(state.id)
        if state_delete:
            StateInMinorFaction.objects.filter(id__in=state_delete).delete()
        if state_add:
            StateInMinorFaction.objects.bulk_create(state_add)
        
    def create_dipendent(self, instance, validated_data):
        self.create_state(instance, validated_data)

    def update_dipendent(self, instance, validated_data):
        self.update_state(instance, validated_data)

    def update_or_create(self, validated_data):
        minorFaction, create = create_or_update_if_time(
            MinorFaction, time=self.get_time(validated_data),
            defaults=self.get_data_defaults(validated_data),
            defaults_create=self.get_data_defaults_create(validated_data), 
            defaults_update=self.get_data_defaults_update(validated_data), 
            name=validated_data.get('Name'),
        )
        def_create_dipendent = lambda instance: self.create_dipendent(instance, validated_data)
        def_update_dipendent = lambda instance: self.update_dipendent(instance, validated_data)
        instance, create = create_or_update_if_time(
            MinorFactionInSystem, time=self.get_time(validated_data), 
            defaults=self.get_data_defaults(validated_data, self.set_data_defaults_MinorFactionInSystem),
            defaults_create=self.get_data_defaults_create(validated_data), 
            defaults_update=self.get_data_defaults_update(validated_data),
            create_function=def_create_dipendent, update_function=def_update_dipendent,
            system=validated_data.get('system'), minorFaction=minorFaction,
        )
        return instance
    
    class Meta:
        list_serializer_class = MinorFactionInSystemListSerializer
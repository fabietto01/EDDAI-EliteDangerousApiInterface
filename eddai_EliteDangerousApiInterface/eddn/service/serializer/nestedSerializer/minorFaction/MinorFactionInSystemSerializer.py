from rest_framework import serializers
from django.db import OperationalError, ProgrammingError

from eddn.service.serializer.nestedSerializer.minorFaction.BaseMinorFactionSerializer import BaseMinorFactionSerializer

from core.utility import (
    create_or_update_if_time, in_list_models, 
    get_or_none
)
from core.api.fields import CacheSlugRelatedField

from ed_bgs.models import (
    Faction, Government, MinorFaction, 
    MinorFactionInSystem, State,
    StateInMinorFaction
)

from eddn.service.serializer.nestedSerializer.StateSerializer import StateSerializer


class MinorFactionInSystemSerializer(BaseMinorFactionSerializer):
    Allegiance = CacheSlugRelatedField(
        queryset=Faction.objects.all(),
        slug_field='eddn',
    )
    Government = CacheSlugRelatedField(
        queryset=Government.objects.all(),
        slug_field='eddn',
    )
    Influence = serializers.FloatField(
        min_value=0, max_value=1,
    )
    Happiness = CacheSlugRelatedField(
        queryset=State.objects.filter(type=State.TypeChoices.HAPPINESS.value),
        slug_field='eddn',
        allow_null=True,
    )
    RecoveringStates = serializers.ListField(
        child=StateSerializer(),
        min_length = 1,
        required = False,
    )
    ActiveStates = serializers.ListField(
        child=StateSerializer(),
        min_length = 1,
        required = False,
    )
    PendingStates = serializers.ListField(
        child=StateSerializer(),
        min_length = 1,
        required = False,
    )

    def set_data_defaults_minorFaction(self, validated_data: dict) -> dict:
        return {
            "allegiance": get_or_none(Faction, eddn=validated_data.get('Allegiance')),
            "government": get_or_none(Government, eddn=validated_data.get('Government')),
        }
    
    def set_data_defaults_MinorFactionInSystem(self, validated_data: dict) -> dict:
        return {
            "Influence": validated_data.get('Influence'),
        }

    def data_preparation(self, validated_data: dict) -> dict:
        self.stato_data = {
            "Happiness": validated_data.get('Happiness', None),
            'RecoveringStates': validated_data.get('RecoveringStates', []),
            'ActiveStates': validated_data.get('ActiveStates', []),
            'PendingStates': validated_data.get('PendingStates', [])
        }

    def create_state(self, instance):
        """
        metodo chiamato quando ll'istanza è creata quindi si occupa di creare
        gli stati corellatti al istanza
        """
        stateAddList = []
        self.populate_models_list(stateAddList, instance)
        if stateAddList:
            StateInMinorFaction.objects.bulk_create(stateAddList)

    def update_state(self, instance):
        """
        medoto chiamato quando l'istanza è aggiornata quindi si occupa di aggiornare
        gli stati corellati al istanza
        """
        stateAddList = []
        stateRemoveList = []
        stateList = []
        self.populate_models_list(stateList, instance)
        stateQsList = list(StateInMinorFaction.objects.filter(minorFaction=instance))
        for state in stateList:
            if not in_list_models(state, stateQsList):
                stateAddList.append(state)
        for state in stateQsList:
            if not in_list_models(state, stateList):
                stateRemoveList.append(state.id)
        if stateAddList:
            StateInMinorFaction.objects.bulk_create(stateAddList)
        if stateRemoveList:
            StateInMinorFaction.objects.filter(id__in=stateRemoveList).delete()

    def populate_models_list(self, list:list, instance) -> list:
        """
        metodo che popola la lista di istanze da creare o aggiornare
        """
        if self.stato_data.get('Happiness', None):
            list.append(
                self.get_state_instance(
                    instance=instance, 
                    state=self.stato_data.get('Happiness', {}).get('State')
                )
            )
        if self.stato_data.get('RecoveringStates', []):
            for state in self.stato_data.get('RecoveringStates', []):
                list.append(
                    self.get_state_instance(
                        instance=instance, 
                        state=State.objects.get(eddn=state.get('State')),
                        phase=StateInMinorFaction.PhaseChoices.RECOVERING.value
                    )
                )
        if self.stato_data.get('ActiveStates', []):
            for state in self.stato_data.get('ActiveStates', []):
                list.append(
                    self.get_state_instance(
                        instance=instance, 
                        state=State.objects.get(eddn=state.get('State')),
                        phase=StateInMinorFaction.PhaseChoices.ACTIVE.value
                    )
                )
        if self.stato_data.get('PendingStates', []):
            for state in self.stato_data.get('PendingStates', []):
                list.append(
                    self.get_state_instance(
                        instance=instance, 
                        state=State.objects.get(eddn=state.get('State')),
                        phase=StateInMinorFaction.PhaseChoices.PENDING.value
                    )
                )

    def get_state_instance(self, instance:MinorFactionInSystem, state:State, phase:str=StateInMinorFaction.PhaseChoices.ACTIVE.value) -> StateInMinorFaction:
        return StateInMinorFaction(
            minorFaction=instance, state=state, 
            phase=phase, created_by=self.agent, updated_by=self.agent
        )

    def create_dipendent(self, instance):
        self.create_state(instance)

    def update_dipendent(self, instance):
        self.update_state(instance)

    def update_or_create(self, validated_data: dict):
        minorFaction, create = create_or_update_if_time(
            MinorFaction, time=self.get_time(validated_data),
            defaults_create=self.get_data_defaults_create(), defaults_update=self.get_data_defaults_update(), 
            defaults=self.get_data_defaults(validated_data, self.set_data_defaults_minorFaction),
            name=validated_data.get('Name'),
        )
        self.data_preparation(validated_data)
        self.instance, create = create_or_update_if_time(
            MinorFactionInSystem, time=self.get_time(validated_data), 
            defaults=self.get_data_defaults(validated_data, self.set_data_defaults_MinorFactionInSystem),
            defaults_create=self.get_data_defaults_create(), defaults_update=self.get_data_defaults_update(),
            create_function=self.create_dipendent, update_function=self.update_dipendent,
            system=validated_data.get('system'), minorFaction=minorFaction,
        )
        return self.instance
from rest_framework import serializers

from ..baseSerializer import BaseListSerializer

from .stateSerializer import StateSerializer

from ed_bgs.models import Faction, Government, State, MinorFactionInSystem, MinorFaction

class ListMinorFactionInSystemSerializer(BaseListSerializer):

    def validate(self, attrs):
        count = len(attrs)
        if count > MinorFactionInSystem.get_max_relations():
            raise serializers.ValidationError(f"too many factions in system: {count}")
        return super().validate(attrs)
    
    def create_minorFaction(self, data:list[dict]) -> list[MinorFaction]:
        qs = MinorFaction.objects.all()
        minorFaction_add:list[MinorFaction] = []
        minorFaction_update:list[MinorFaction] = []
        for data in data:
            try:
                minorFaction = qs.get(name=data.get("name"))
                data.pop("name")
                for key, value in data.items():
                    setattr(minorFaction, key, value)
                minorFaction_update.append(minorFaction)
            except MinorFaction.DoesNotExist:
                minorFaction_add.append(MinorFaction(**data))
        minorFaction_list = []
        if minorFaction_add:
            minorFaction_list = MinorFaction.objects.bulk_create(minorFaction_add)
        if minorFaction_update:
            MinorFaction.objects.bulk_update(minorFaction_update)
            minorFaction_list.extend(minorFaction_update)
        return minorFaction_list
    
    def create_minorFactionInSystem(self, instance, data:list[dict]) -> list[MinorFactionInSystem]:
        qs = MinorFactionInSystem.objects.filter(system=instance)
        minorFactionInSystem_add:list[MinorFactionInSystem] = []
        minorFactionInSystem_update:list[MinorFactionInSystem] = []
        for data in data:
            try:
                minorFactionInSystem = qs.get(minorFaction=data.get("minorFaction"))
                for key, value in data.items():
                    setattr(minorFactionInSystem, key, value)
                minorFactionInSystem_update.append(minorFactionInSystem)
            except MinorFactionInSystem.DoesNotExist:
                minorFactionInSystem_add.append(MinorFactionInSystem(system=instance, **data))
        minorFactionInSystem_list = []
        if minorFactionInSystem_add:
            minorFactionInSystem_list = MinorFactionInSystem.objects.bulk_create(minorFactionInSystem_add)
        if minorFactionInSystem_update:
            MinorFactionInSystem.objects.bulk_update(minorFactionInSystem_update)
            minorFactionInSystem_list.extend(minorFactionInSystem_update)
        return minorFactionInSystem_list

    def update(self, instance, validated_data:list[dict]):
        fields = self.get_fields_materilFaciotn(MinorFaction)
        data = []
        for item in validated_data:
            data.append({key: value for key, value in item.items() if key in fields})
        minorFaction_list = self.create_minorFaction(data)
        fields = self.get_fields_materilFaciotn(MinorFactionInSystem)
        data = []
        for item in validated_data:
            faction_name = item.get("name")
            minorFaction = next((faction for faction in minorFaction_list if faction.name == faction_name), None)
            {key: value for key, value in item.items() if key in fields}
        return self.create_minorFactionInSystem(instance, data)

class MinorFactionInSystemSerializer(serializers.ModelSerializer):
    Name = serializers.CharField(
        min_length=1,
        source="name"
    )
    Allegiance = serializers.SlugRelatedField(
        queryset=Faction.objects.all(),
        slug_field='eddn',
        source="allegiance"
    )
    Government = serializers.SlugRelatedField(
        queryset=Government.objects.all(),
        slug_field='eddn',
        source="government"
    )
    Influence = serializers.FloatField(
        min_value=0, max_value=1,
    )
    # Happiness = serializers.SlugRelatedField(
    #     queryset=State.objects.filter(type=State.TypeChoices.HAPPINESS.value),
    #     slug_field='eddn',
    #     allow_null=True,
    # )
    # RecoveringStates = StateSerializer(
    #     many=True,
    #     required = False,
    # )
    # ActiveStates = StateSerializer(
    #     many=True,
    #     required = False,
    # )
    # PendingStates = StateSerializer(
    #     many=True,
    #     required = False,
    # )

    def validate(self, attrs):
        return super().validate(attrs)
    
    def save(self, **kwargs):
        return super().save(**kwargs)
    
    def create(self, validated_data):
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)

    class Meta:
        model = MinorFactionInSystem
        list_serializer_class = ListMinorFactionInSystemSerializer
        fields = [
            'Name', 'Allegiance',
            "Government", "Influence",
        ]
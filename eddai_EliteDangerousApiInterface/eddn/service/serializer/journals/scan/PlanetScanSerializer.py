from rest_framework import serializers
from eddn.service.serializer.journals.scan.BaseScanSerializer import BaseScanSerializer

from core.utility import get_values_list_or_default, get_or_none, in_list_models
from core.api.fields import CacheChoiceField
from django.db import OperationalError, ProgrammingError
from eddn.service.serializer.customFields import ReserveLevelChoiceField

from ed_body.models import Planet, AtmosphereType, PlanetType, Volcanism, AtmosphereComponentInPlanet, AtmosphereComponent
from ed_material.models import Material, MaterialInPlanet

from eddn.service.serializer.journals.scan.nestedScan import MaterialsSerializer, AtmosphereComponentSerializer, CompositionSerializers

import uuid

class PlanetScanSerializer(BaseScanSerializer):
    
    AtmosphereType = CacheChoiceField(
        fun_choices=lambda: get_values_list_or_default(AtmosphereType, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
        cache_key=AtmosphereType.get_cache_key(),
        required=False,
    )
    PlanetClass = CacheChoiceField(
        fun_choices=lambda: get_values_list_or_default(PlanetType, [], (OperationalError, ProgrammingError), 'name', flat=True),
        cache_key=PlanetType.get_cache_key(),
        required=False,
    )
    Volcanism = CacheChoiceField(
        fun_choices=lambda: get_values_list_or_default(Volcanism, [], (OperationalError, ProgrammingError), 'eddn', flat=True),
        cache_key=Volcanism.get_cache_key(),
        allow_blank=True,
        required=False,
    )
    TerraformState = serializers.ChoiceField(
        choices=Planet.TerraformingState.choices,
        allow_blank=True,
        required=False,
    )
    Composition = CompositionSerializers(
        required=False,
    )
    Landable = serializers.BooleanField(
        required=False,
    )
    MassEM = serializers.FloatField(
        min_value=0,
        required=False,
    )
    SurfaceGravity = serializers.FloatField(
        min_value=0,
        required=False,
    )
    SurfacePressure = serializers.FloatField(
        min_value=0,
        required=False,
    )
    TidalLock = serializers.BooleanField(
        required=False,
    )
    ReserveLevel = ReserveLevelChoiceField(
        choices=Planet.ReserveLevel.choices,
        required=False,
    )
    Materials = serializers.ListField(
        child=MaterialsSerializer(),
        required=False,
    )
    AtmosphereComposition = serializers.ListField(
        child=AtmosphereComponentSerializer(),
        required=False,
    )

    def data_preparation(self, validated_data: dict) -> dict:
        super().data_preparation(validated_data)
        self.materials_data:dict = validated_data.pop('Materials', None)
        self.atmosphereComposition_data:dict = validated_data.pop('AtmosphereComposition', None)

    def update_atmosphereComposition(self, instance):
        atmosphereCompositionList = [
            AtmosphereComponentInPlanet(
                atmosphere_component=AtmosphereComponent.objects.get(eddn=atmosphereComponent.get('Name')),
                percent=atmosphereComponent.get('Percent'),
                planet=instance,
                created_by=self.agent, updated_by=self.agent
            ) for atmosphereComponent in self.atmosphereComposition_data
        ]
        atmosphereCompositionAddList = []
        atmosphereCompositionDeleteList = []
        atmosphereCompositionQs = AtmosphereComponentInPlanet.objects.filter(planet=instance)
        for atmosphereComponent in atmosphereCompositionList:
            if not in_list_models(atmosphereComponent, atmosphereCompositionQs):
                atmosphereCompositionAddList.append(atmosphereComponent)
        for atmosphereComponent in atmosphereCompositionQs:
            if not in_list_models(atmosphereComponent, atmosphereCompositionList):
                atmosphereCompositionDeleteList.append(atmosphereComponent.id)
        if atmosphereCompositionAddList:
            AtmosphereComponentInPlanet.objects.bulk_create(atmosphereCompositionAddList)
        if atmosphereCompositionDeleteList:
            AtmosphereComponentInPlanet.objects.filter(id__in=atmosphereCompositionDeleteList).delete()

    def update_materials(self, instance):
        materialsList = [
            MaterialInPlanet(
                planet=instance, 
                material=Material.objects.get(name=material.get('Name')),
                percent=material.get('Percent'),
                created_by=self.agent, updated_by=self.agent
            )  for material in self.materials_data
        ]
        materialsAddList = []
        materialsDeleteList = []
        materialQs = MaterialInPlanet.objects.filter(planet=instance)
        for material in materialsList:
            if not in_list_models(material, materialQs):
                materialsAddList.append(material)
        for material in materialQs:
            if not in_list_models(material, materialsList):
                materialsDeleteList.append(material.id)
        if materialsAddList:
            MaterialInPlanet.objects.bulk_create(materialsAddList)
        if materialsDeleteList:
            MaterialInPlanet.objects.filter(id__in=materialsDeleteList).delete()
        
    def set_data_defaults(self, validated_data: dict) -> dict:
        defaults = super().set_data_defaults(validated_data)
        composition:dict = validated_data.get('Composition', {})
        defaults.update({
            'atmosphereType': get_or_none(AtmosphereType, eddn=validated_data.get('AtmosphereType', None)),	
            'planetType': get_or_none(PlanetType, name=validated_data.get('PlanetClass', None)),
            'volcanism': get_or_none(Volcanism, eddn=validated_data.get('Volcanism', None)),
            'terraformState': validated_data.get('TerraformState', None),
            'landable': validated_data.get('Landable', None),
            '_compositionIce': composition.get('Ice', None),
            '_compositionRock': composition.get('Rock', None),
            '_compositionMetal': composition.get('Metal', None),
            'massEM': validated_data.get('MassEM', None),
            'surfaceGravity': validated_data.get('SurfaceGravity', None),
            'surfacePressure': validated_data.get('SurfacePressure', None),
            'tidalLock': validated_data.get('TidalLock', None),
            'reserveLevel': validated_data.get('ReserveLevel', None),
        })
        return defaults

    def create_dipendent(self, instance):
        if self.materials_data:
            self.update_materials(instance)
        if self.atmosphereComposition_data:
            self.update_atmosphereComposition(instance)
        super().create_dipendent(instance)

    def update_dipendent(self, instance):
        if self.materials_data:
            self.update_materials(instance)
        if self.atmosphereComposition_data:
            self.update_atmosphereComposition(instance)
        super().update_dipendent(instance)

    class Meta:
        model = Planet

from rest_framework import serializers
from eddn.service.journals.scan.BaseScanSerializer import BaseScanSerializer

from core.utility import get_values_list_or_default, get_or_none, in_list_models
from django.db import OperationalError, ProgrammingError
from eddn.service.seriallizers.customFields.CustomChoiceField import ReserveLevelChoiceField

from ed_body.models import Planet, AtmosphereType, PlanetType, Volcanism, MaterialInPlanet, AtmosphereComponentInPlanet, AtmosphereComponent
from ed_material.models.Material import Material

from eddn.service.journals.scan.MaterialsSerializer import MaterialsSerializer
from eddn.service.journals.scan.AtmosphereComponentSerializer import AtmosphereComponentSerializer
from eddn.service.journals.scan.CompositionSerializers import CompositionSerializers

class PlanetScanSerializer(BaseScanSerializer):
    
    AtmosphereType = serializers.ChoiceField(
        choices=get_values_list_or_default(AtmosphereType, [], (OperationalError, ProgrammingError), 'eddn', flat=True)
    )
    PlanetClass = serializers.ChoiceField(
        choices=get_values_list_or_default(PlanetType, [], (OperationalError, ProgrammingError), 'name', flat=True)
    )
    Volcanism = serializers.ChoiceField(
        choices=get_values_list_or_default(Volcanism, [], (OperationalError, ProgrammingError), 'name', flat=True)
    )
    TerraformState = serializers.ChoiceField(
        choices=Planet.TerraformingState.choices,
    )
    Composition = CompositionSerializers()
    Landable = serializers.BooleanField()
    MassEM = serializers.FloatField(
        min_value=0,
    )
    SurfaceGravity = serializers.FloatField(
        min_value=0,
    )
    SurfacePressure = serializers.FloatField(
        min_value=0,
    )
    TidalLock = serializers.BooleanField()
    ReserveLevel = ReserveLevelChoiceField(
        choices=Planet.ReserveLevel.choices,
    )
    Materials = serializers.ListField(
        child=MaterialsSerializer(),
    )
    AtmosphereComposition = serializers.ListField(
        child=AtmosphereComponentSerializer(),
    )

    def data_preparation(self, validated_data: dict) -> dict:
        self.materials_data:dict = validated_data.pop('Materials')
        self.atmosphereComposition_data:dict = validated_data.pop('AtmosphereComposition')
        return BaseScanSerializer.data_preparation(self, validated_data)

    def update_atmosphereComposition(self, instance):
        atmosphereCompositionList = [
            AtmosphereComponentInPlanet(
                atmosphereComponent=AtmosphereComponent.objects.get(name=atmosphereComponent.get('Name')),
                percent=atmosphereComponent.get('Percent'),
                planet=instance,
            ) for atmosphereComponent in self.atmosphereComposition_data
        ]
        atmosphereCompositionAddList = []
        atmosphereCompositionDeleteList = []
        atmosphereCompositionQs = AtmosphereComponentInPlanet.objects.filter(planet=instance)
        atmosphereCompositionQSList = list(atmosphereCompositionQs)
        for atmosphereComponent in atmosphereCompositionList:
            if not in_list_models(atmosphereComponent, atmosphereCompositionQSList):
                atmosphereCompositionAddList.append(atmosphereComponent)
        for atmosphereComponent in atmosphereCompositionQSList:
            if not in_list_models(atmosphereComponent, atmosphereCompositionList):
                atmosphereCompositionDeleteList.append(atmosphereComponent)
        if atmosphereCompositionAddList:
            AtmosphereComponentInPlanet.objects.bulk_create(atmosphereCompositionAddList)
        if atmosphereCompositionDeleteList:
            AtmosphereComponentInPlanet.objects.filter(id__in=[atmosphereComponent.id for atmosphereComponent in atmosphereCompositionDeleteList]).delete()

    def update_materials(self, instance):
        materialsList = [
            MaterialInPlanet(
                planet=instance, 
                material=Material.objects.get(name=material.get('Name')),
                percent=material.get('Percent'),
            )  for material in self.materials_data
        ]
        materialsAddList = []
        materialsDeleteList = []
        materialQs = MaterialInPlanet.objects.filter(planet=instance)
        materialQSList = list(materialQs)
        for material in materialsList:
            if not in_list_models(material, materialQSList):
                materialsAddList.append(material)
        for material in materialQSList:
            if not in_list_models(material, materialsList):
                materialsDeleteList.append(material)
        if materialsAddList:
            MaterialInPlanet.objects.bulk_create(materialsAddList)
        if materialsDeleteList:
            MaterialInPlanet.objects.filter(id__in=[material.id for material in materialsDeleteList]).delete()
        
    def set_data_defaults(self, validated_data: dict) -> dict:
        defaults = BaseScanSerializer.set_data_defaults(self, validated_data)
        composition:dict = validated_data.get('Composition')
        defaults.update({
            'atmosphereType': get_or_none(AtmosphereType, name=validated_data.get('AtmosphereType')),
            'planetType': get_or_none(PlanetType, name=validated_data.get('PlanetClass')),
            'volcanism': get_or_none(Volcanism, name=validated_data.get('Volcanism')),
            'terraformState': validated_data.get('TerraformState'),
            'landable': validated_data.get('Landable'),
            '_compositionIce': composition.get('Ice'),
            '_compositionRock': composition.get('Rock'),
            '_compositionMetal': composition.get('Metal'),
            'massEM': validated_data.get('MassEM'),
            'surfaceGravity': validated_data.get('SurfaceGravity'),
            'surfacePressure': validated_data.get('SurfacePressure'),
            'tidalLock': validated_data.get('TidalLock'),
            'reserveLevel': validated_data.get('ReserveLevel'),
        })

    def create_dipendent(self, instance):
        if self.materials_data:
            self.update_materials(instance)
        if self.atmosphereComposition_data:
            self.update_atmosphereComposition(instance)
        BaseScanSerializer.create_dipendent(self, instance)

    def update_dipendent(self, instance):
        if self.materials_data:
            self.update_materials(instance)
        if self.atmosphereComposition_data:
            self.update_atmosphereComposition(instance)
        BaseScanSerializer.update_dipendent(self, instance)

    class Meta:
        model = Planet

from rest_framework import serializers
from .baseScanSerializer import BaseScanSerializer

from ...nestedSerializers import CompositionSerializers, MaterialsSerializer, AtmosphereComponentSerializer
from ...customFields import ReserveLevelChoiceField

from ed_body.models import Planet, AtmosphereType, PlanetType, Volcanism, AtmosphereComponentInPlanet, AtmosphereComponent

from core.utility import create_or_update_if_time

class PlanetScanSerializer(BaseScanSerializer):
    AtmosphereType = serializers.SlugRelatedField(
        queryset=AtmosphereType.objects.all(),
        slug_field='eddn',
        required=False,
    )
    PlanetClass = serializers.SlugRelatedField(
        queryset=PlanetType.objects.all(),
        slug_field='name',
        required=False,
    )
    Volcanism = serializers.SlugRelatedField(
        queryset=Volcanism.objects.all(),
        slug_field='eddn',
        required=False,
        allow_null=True,
    )
    TerraformState = serializers.ChoiceField(
        choices=Planet.TerraformingState.choices,
        required=False,
        allow_null=True,
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
        required=False,
    )
    Materials = MaterialsSerializer(
        many=True,
        required=False,
    )
    AtmosphereComposition = AtmosphereComponentSerializer(
        many=True,
        required=False,
    )

    def _get_composition(self, validated_data) -> dict:
        return validated_data.get('Composition', None)
    
    def _get_composition_ice(self, validated_data) -> dict:
        composition = self._get_composition(validated_data)
        if composition:
            return composition.get('Ice', None)
        return None
    
    def _get_composition_rock(self, validated_data) -> dict:
        composition = self._get_composition(validated_data)
        if composition:
            return composition.get('Rock', None)
        return None
    
    def _get_composition_metal(self, validated_data) -> dict:
        composition = self._get_composition(validated_data)
        if composition:
            return composition.get('Metal', None)
        return None

    def set_data_defaults_body(self, validated_data: dict) -> dict:
        defaults = super().set_data_defaults_body(validated_data)
        defaults.update(
            {
                "atmosphereType": validated_data.get('AtmosphereType', None),
                "planetType": validated_data.get('PlanetClass', None),
                "volcanism": validated_data.get('Volcanism', None),
                "terraformState": validated_data.get('TerraformState', None),
                "landable": validated_data.get('Landable', None),
                '_compositionIce': self._get_composition_ice(validated_data),
                '_compositionRock': self._get_composition_rock(validated_data),
                '_compositionMetal': self._get_composition_metal(validated_data),
                "massEM": validated_data.get('MassEM', None),
                "surfaceGravity": validated_data.get('SurfaceGravity', None),
                "surfacePressure": validated_data.get('SurfacePressure', None),
                "tidalLock": validated_data.get('TidalLock', None),
                "reserveLevel": validated_data.get('ReserveLevel', None),
            }
        )
        return defaults
    
    def run_update_materials(self, instance, validated_data):
        if validated_data.get('Materials', None):
            serializer = MaterialsSerializer(data=self.initial_data.get('Materials', []), many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(
                created_by=validated_data.get('created_by'),
                updated_by=validated_data.get('updated_by'),
                updated_at=validated_data.get('updated_at'),
                planet=instance,
            )

    def run_update_atmosphereComposition(self, instance, validated_data):
        if validated_data.get('AtmosphereComposition', None):
            serializer = AtmosphereComponentSerializer(data=self.initial_data.get('AtmosphereComposition', []), many=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(
                created_by=validated_data.get('created_by'),
                updated_by=validated_data.get('updated_by'),
                updated_at=validated_data.get('updated_at'),
                planet=instance,
            )
    
    def create_dipendent(self, instance, validated_data):
        super().create_dipendent(instance, validated_data)
        self.run_update_materials(instance, validated_data)
        self.run_update_atmosphereComposition(instance, validated_data)

    def update_dipendent(self, instance, validated_data):
        super().update_dipendent(instance, validated_data)
        self.run_update_materials(instance, validated_data)
        self.run_update_atmosphereComposition(instance, validated_data)

    class Meta:
        model = Planet
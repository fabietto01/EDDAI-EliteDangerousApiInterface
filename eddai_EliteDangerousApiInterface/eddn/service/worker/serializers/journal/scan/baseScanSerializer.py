from rest_framework import serializers
from ..baseJournalSerializer import BaseJournalSerializer

from ed_body.models import BaseBody
from ...nestedSerializers import RingSerializer

from core.utility import create_or_update_if_time

class BaseScanSerializer(BaseJournalSerializer):
    BodyName = serializers.CharField(
        max_length=255,
    )
    DistanceFromArrivalLS = serializers.FloatField(
        min_value=0,
    )
    Radius = serializers.FloatField(
        min_value=0,
        required=False,
    )
    SurfaceTemperature = serializers.FloatField(
        min_value=0,
        required=False,
    )
    BodyID = serializers.IntegerField(
        min_value=0,
    )
    AxialTilt = serializers.FloatField(
        min_value=-360,
        max_value=360,
        required=False,
    )
    RotationPeriod = serializers.FloatField(
        required=False,
    )
    Eccentricity = serializers.FloatField(
        min_value=0,
        max_value=1,
        required=False,
    )
    OrbitalInclination = serializers.FloatField(
        min_value=-360,
        max_value=360,
        required=False,
    )
    OrbitalPeriod = serializers.FloatField(
        min_value=0,
        required=False,
    )
    Periapsis = serializers.FloatField(
        required=False,
    )
    SemiMajorAxis = serializers.FloatField(
        min_value=0,
        required=False,
    )
    AscendingNode = serializers.FloatField(
        required=False,
    )
    MeanAnomaly = serializers.FloatField(
        required=False,
    )
    Rings = RingSerializer(
        many=True,
        required=False,
    )
    Parents = serializers.ListField(
        child=serializers.JSONField(),
        min_length=1,
        required=False,
    )

    def _get_parent_id(self, data):
        parents:list[dict] = data.get('Parents', None)
        if parents:
            return list(parents[0].values())[0]
        return None

    def set_data_defaults_body(self, validated_data):
        return {
            'distance': validated_data.get('DistanceFromArrivalLS'),
            'radius': validated_data.get('Radius', None),
            'surfaceTemperature': validated_data.get('SurfaceTemperature', None),
            'axialTilt': validated_data.get('AxialTilt', None),
            'rotationPeriod': validated_data.get('RotationPeriod', None),
            'eccentricity': validated_data.get('Eccentricity', None),
            'orbitalInclination': validated_data.get('OrbitalInclination', None),
            'orbitalPeriod': validated_data.get('OrbitalPeriod', None),
            'periapsis': validated_data.get('Periapsis', None),
            'semiMajorAxis': validated_data.get('SemiMajorAxis', None),
            'ascendingNode': validated_data.get('AscendingNode', None),
            'meanAnomaly': validated_data.get('MeanAnomaly', None),
            'parentsID': self._get_parent_id(validated_data),
        }
    
    def run_save_ring(self, instance, validated_data):
        for ring in self.initial_data.get('Rings', []):
            serializers = RingSerializer(data=ring)
            serializers.is_valid(raise_exception=True)
            serializers.save(
                created_by=validated_data.get('created_by'),
                updated_by=validated_data.get('updated_by'),
                updated_at=validated_data.get('updated_at'),
                body=instance
            )

    def create_dipendent(self, instance, validated_data):
        self.run_save_ring(instance, validated_data)

    def update_dipendent(self, instance, validated_data):
        self.run_save_ring(instance, validated_data)

    def update_or_create(self, validated_data, update_function=None, create_function=None):
        system = super().update_or_create(validated_data, update_function, create_function)
        def_create_dipendent = lambda instance: self.create_dipendent(instance, validated_data)
        def_update_dipendent = lambda instance: self.update_dipendent(instance, validated_data)
        ModelClass:BaseBody = self.Meta.model
        body, create = create_or_update_if_time(
            ModelClass, time=self.get_time(),
            defaults=self.get_data_defaults(validated_data, self.set_data_defaults_body),
            defaults_create=self.get_data_defaults_create(validated_data),
            defaults_update=self.get_data_defaults_update(validated_data),
            update_function=def_update_dipendent,
            create_function=def_create_dipendent,
            system=system, name=validated_data.get('BodyName'), bodyID=validated_data.get('BodyID')
        )
        return body

    class Meta:
        model = BaseBody
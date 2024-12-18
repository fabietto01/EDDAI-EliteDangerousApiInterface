from rest_framework import serializers
from eddn.service.serializer.journals.BaseJournal import BaseJournal

from core.utility import create_or_update_if_time

from eddn.service.serializer.nestedSerializer import RingSerializer
from ed_system.models import System
from ed_body.models import BaseBody

class BaseScanSerializer(BaseJournal):
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
    Parents = serializers.ListField(
        child=serializers.JSONField(),
        min_length=1,
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
    Rings = serializers.ListField(
        child=RingSerializer(),
        min_length=1,
        required=False,
    )
    Parents = serializers.ListField(
        child=serializers.JSONField(),
        min_length=1,
        required=False,
    )

    def set_data_defaults_system(self, validated_data: dict) -> dict:
        return BaseJournal.set_data_defaults(self, validated_data)

    def set_data_defaults(self, validated_data: dict) -> dict:
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
            'parentsID': list(validated_data.get('Parents', None)[0].values())[0] if validated_data.get('Parents', None) else None,
        }

    def data_preparation(self, validated_data: dict) -> dict:
        self.rings_data:dict = validated_data.pop('Rings', None)

    def update_ring(self, instance):
        for ring_data in self.rings_data:
            serializer = RingSerializer(data=ring_data)
            if serializer.is_valid():
                serializer.save(
                    body=instance, timestamp=self.get_time()
                )

    def create_dipendent(self, instance):
        if self.rings_data:
            self.update_ring(instance)

    def update_dipendent(self, instance):
        if self.rings_data:
            self.update_ring(instance)

    def update_or_create(self, validated_data: dict, update_function=None, create_function=None):
        system, create = create_or_update_if_time(
            System, time=self.get_time(validated_data), defaults=self.get_data_defaults(validated_data, self.set_data_defaults_system),
            defaults_create=self.get_data_defaults_create(), defaults_update=self.get_data_defaults_update(),
            name=validated_data.get('StarSystem')
        )
        self.data_preparation(validated_data)
        ModelClass:BaseBody = self.Meta.model
        body, create = create_or_update_if_time(
            ModelClass,  time=self.get_time(validated_data), defaults=self.get_data_defaults(validated_data),
            defaults_create=self.get_data_defaults_create(), defaults_update=self.get_data_defaults_update(),
            create_function=self.create_dipendent, update_function=self.update_dipendent,
            system=system, name=validated_data.get('BodyName'), bodyID=validated_data.get('BodyID')
        )
        return body

    class Meta:
        model = BaseBody
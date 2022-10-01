from rest_framework import serializers
from eddn.service.journals.BaseJournal import BaseJournal

from core.utility import update_or_create_if_time, get_values_list_or_default, get_or_none
from django.db import OperationalError, ProgrammingError

class BaseScan(BaseJournal):
        
    BodyName = serializers.CharField(
        max_length=255,
    )
    DistanceFromArrivalLS = serializers.FloatField(
        min_value=0,
    )

    Radius = serializers.FloatField(
        min_value=0,
    )
    SurfaceTemperature = serializers.FloatField(
        min_value=0,
    )
    BodyID = serializers.IntegerField(
        min_value=0,
    )
    AxialTilt = serializers.FloatField(
        min_value=-360,
        max_value=360,
    )
    RotationPeriod = serializers.FloatField(
        min_value=0,
    )
    Eccentricity = serializers.FloatField(
        min_value=0,
        max_value=1,
    )
    OrbitalInclination = serializers.FloatField(
        min_value=-360,
        max_value=360,
    )
    OrbitalPeriod = serializers.FloatField(
        min_value=0,
    )
    Periapsis = serializers.FloatField()
    SemiMajorAxis = serializers.FloatField(
        min_value=0,
    )
    AscendingNode = serializers.FloatField()
    MeanAnomaly = serializers.FloatField()
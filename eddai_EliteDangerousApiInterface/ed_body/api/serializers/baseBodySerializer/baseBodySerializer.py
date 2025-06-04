from ._baseBodySerializer import _BaseBodySerializer
from ed_core.api.serializers.DistanceSerializer import DistanceSerializer

from ..planetSerializer import PlanetSerializer, PlanetDistanceSerializer
from ..starSerializer import StarSerializer, StarDistanceSerializer

from ed_body.models import (
    Star, Planet
)

class BaseBodySerializer(_BaseBodySerializer):
    
    def to_representation(self, instance):
        if isinstance(instance, Planet):
            return PlanetSerializer(instance).data
        elif isinstance(instance, Star):
            return StarSerializer(instance).data
        return super().to_representation(instance)

class BaseBodyDistanceSerializer(BaseBodySerializer, DistanceSerializer):
        
    def to_representation(self, instance):
        if isinstance(instance, Planet):
            return PlanetDistanceSerializer(instance).data
        elif isinstance(instance, Star):
            return StarDistanceSerializer(instance).data
        return super().to_representation(instance)
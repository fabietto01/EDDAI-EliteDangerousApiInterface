from .StationSerializer import StationSerializer
from ed_core.api.serializers.DistanceSerializer import DistanceSerializer

class StationDistanceSerializer(StationSerializer, DistanceSerializer ):
    pass
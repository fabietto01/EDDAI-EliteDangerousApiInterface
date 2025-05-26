from django.test import TestCase

from ed_station.models import (
    Service,
    ServiceInStation,
    Station,
    StationType,
)

from ed_station.api.serializers import (
    StationSerializer, StationDistanceSerializer,
    StationBasicInformation,
    StationTypeBasicInformationSerializer,
    ServiceInStationSerializer,
)
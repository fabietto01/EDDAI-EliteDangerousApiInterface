from rest_framework.test import APITestCase

from ed_station.models import (
    Service,
    ServiceInStation,
    Station,
    StationType,
)

from ed_station.api.serializers import (
    StationSerializer, StationDistanceSerializer,
    StationBasicInformation,
    StationTypeBasicInformationSerializer, StationTypeSerializer,
    ServiceInStationSerializer,
)
from ed_system.models import System
from users.models import User

from django.db.models import F
from django.db.models.functions import Round
from ed_core.functions import Distanza3D


BASE_STATION_SERIALIZER_DATA = {
      "id": 2042,
      "system": {
        "id": 11,
        "name": "Sol"
      },
      "type": {
        "id": 5,
        "name": "Orbis"
      },
      "primaryEconomy": {
        "id": 8,
        "name": "Service"
      },
      "secondaryEconomy": {
        "id": 17,
        "name": "None"
      },
      "minorFaction": {
        "id": 3163,
        "name": "Mother Gaia"
      },
      "service": [
        "apexinterstellar",
        "autodock",
        "bartender",
        "contacts"
      ],
      "created_at": "2025-05-28T07:59:32.307000Z",
      "updated_at": "2025-05-28T07:59:32.307000Z",
      "name": "Abraham Lincoln",
      "markerid": 128016896,
      "landingPad": "L",
      "distance": 490.665508,
      "created_by": 1,
      "updated_by": 1
    }

BASE_STATION_DESERIALIZER_DATA = {
  "system_id": 11,
  "type_id": 4,
  "primaryEconomy_id": 4,
  "secondaryEconomy_id": 8,
  "minorFaction_id": 3163,
  "service_id": [
    33, 27,2,24,1
  ],
  "name": "Mother Test Station",
  "markerid": 80760457,
  "landingPad": "S",
  "distance": 423
}

BASE_STATION_TYPE_BASE_SERIALIZER_DATA = {
    "id": 3,
    "name": "Coriolis"
}

BASE_STATION_TYPE_BASE_DESERIALIZER_DATA ={
    "name": "Test BASE Station Type"
}

BASE_STATION_TYPE_SERIALIZER_DATA = {
    "id": 3,
    "name": "Coriolis",
    "description": '',
}

BASE_STATION_TYPE_DESERIALIZER_DATA = {
    "name": "Test Station Type",
    "description": "This is a test description for the station type."
}

BASE_SERVICE_IN_STATION_BASE_SERIALIZER_DATA = {
    "id": 1,
    "service": "apexinterstellar",
}

BASE_SERVICE_IN_STATION_SERIALIZER_DATA = {
      "id": 1,
      "service": "apexinterstellar",
      "created_at": "2025-05-28T07:59:32.323000Z",
      "updated_at": "2025-05-28T07:59:32.323000Z",
      "created_by": 1,
      "updated_by": 1
}

BASE_SERVICE_IN_STATION_DESERIALIZER_DATA = {
    "service": "livery"
}

BASE_MANY_SERVICE_IN_STATION_DESERIALIZER_DATA = [
    {
        "service": "missions"
    },
    {
        "service": "modulepacks"
    }
]

class StationSerializerTestCase(APITestCase):

    fixtures = ['user', 'economy', 'system', 'body', 'bgs', 'station', 'station_test_data']

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the test case.
        This method is called once for the entire test case.
        """
        cls.user = User.objects.create_user(
            username=cls.__class__.__name__,
        )

    def test_serializer(self):
        instance = Station.objects.get(id=2042)
        serializer = StationSerializer(instance)
        data = serializer.data
        self.assertDictEqual(
            data, BASE_STATION_SERIALIZER_DATA,
            msg="The serialized data does not match the expected data."
        )

    def test_deserializer(self):
        serializer = StationSerializer(data=BASE_STATION_DESERIALIZER_DATA)
        is_valid = serializer.is_valid()
        self.assertTrue(
            is_valid,
            msg="The deserialized data is not valid. Errors: {}".format(serializer.errors)
        )
        instance = serializer.save(
            created_by=self.user,
            updated_by=self.user
        )
        for key, value in BASE_STATION_DESERIALIZER_DATA.items():
            if key not in ['body_id', 'type_id', 'primaryEconomy_id', 'secondaryEconomy_id', 'minorFaction_id', 'service_id']:
                self.assertEqual(
                    getattr(instance, key), value,
                    msg=f"The deserialized data does not match the expected data for field '{key}'."
                )
        self.assertEqual(
            instance.body.id, BASE_STATION_DESERIALIZER_DATA["body_id"],
            msg="The deserialized data does not match the expected data for field 'body_id'."
        )
        self.assertEqual(
            instance.type.id, BASE_STATION_DESERIALIZER_DATA["type_id"],
            msg="The deserialized data does not match the expected data for field 'type_id'."
        )
        self.assertEqual(
            instance.primaryEconomy.id, BASE_STATION_DESERIALIZER_DATA["primaryEconomy_id"],
            msg="The deserialized data does not match the expected data for field 'primaryEconomy_id'."
        )
        self.assertEqual(
            instance.secondaryEconomy.id, BASE_STATION_DESERIALIZER_DATA["secondaryEconomy_id"],
            msg="The deserialized data does not match the expected data for field 'secondaryEconomy_id'."
        )
        self.assertEqual(
            instance.minorFaction.id, BASE_STATION_DESERIALIZER_DATA["minorFaction_id"],
            msg="The deserialized data does not match the expected data for field 'minorFaction_id'."
        )
        for service_id in BASE_STATION_DESERIALIZER_DATA["service_id"]:
            self.assertTrue(
                instance.service.filter(id=service_id).exists(),
                msg=f"The deserialized data does not contain the expected service with id '{service_id}'."
            )
            
    def test_many_serializer(self):
        qs = Station.objects.all()
        serializer = StationSerializer(qs, many=True)
        data = serializer.data
        self.assertGreaterEqual(
            len(data), 1,
            msg="The serialized data is empty."
        )

class StationDistanceSerializerTestCase(APITestCase):
    """
    Test case for the StationDistanceSerializer.
    """

    fixtures = ['user', 'economy', 'system', 'body', 'bgs', 'station', 'station_test_data']

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the test case.
        This method is called once for the entire test case.
        """
        cls.system = System.objects.first()

    def test_distance_serializer(self):
        qs = Station.objects.all().annotate(
            distance_st=Round(
                Distanza3D(
                    F('system__coordinate'),
                    point=self.system.coordinate
                ),
                3
            )
        )
        serializer = StationDistanceSerializer(qs, many=True)
        data = serializer.data
        self.assertGreaterEqual(
            len(data), 1,
            msg="The serialized data is empty."
        )
        for item in data:
            self.assertIn('distance_st', item, msg="The 'distance_st' field is missing in the serialized data.")
            distance_calculated = System.get_distance(
                self.system,
                System.objects.get(id=item['system']['id'])
            )
            self.assertEqual(
                item['distance_st'], distance_calculated,
                msg="The 'distance_st' field does not match the expected value."
            )

class StationTypeSerializerTestCase(APITestCase):

    fixtures = ['user', 'economy', 'system', 'body', 'bgs', 'station', 'station_test_data']

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the test case.
        This method is called once for the entire test case.
        """
        cls.user = User.objects.create_user(
            username=cls.__class__.__name__,
        )

    def test_basic_serializer(self):
        instance = StationType.objects.get(id=3)
        serializer = StationTypeBasicInformationSerializer(instance)
        data = serializer.data
        self.assertDictEqual(
            data, BASE_STATION_TYPE_BASE_SERIALIZER_DATA,
            msg="The serialized data does not match the expected data."
        )

    def test_basic_deserializer(self):
        serializer = StationTypeBasicInformationSerializer(data=BASE_STATION_TYPE_BASE_DESERIALIZER_DATA)
        is_valid = serializer.is_valid()
        self.assertTrue(
            is_valid,
            msg="The deserialized data is not valid. Errors: {}".format(serializer.errors)
        )
        instance = serializer.save()
        for key, value in BASE_STATION_TYPE_BASE_DESERIALIZER_DATA.items():
            self.assertEqual(
                getattr(instance, key), value,
                msg=f"The deserialized data does not match the expected data for field '{key}'."
            )

    def test_serializer(self):
        instance = StationType.objects.get(id=3)
        serializer = StationTypeSerializer(instance)
        data = serializer.data
        self.assertDictEqual(
            data, BASE_STATION_TYPE_SERIALIZER_DATA,
            msg="The serialized data does not match the expected data."
        )

    def test_deserializer(self):
        serializer = StationTypeSerializer(data=BASE_STATION_TYPE_DESERIALIZER_DATA)
        is_valid = serializer.is_valid()
        self.assertTrue(
            is_valid,
            msg="The deserialized data is not valid. Errors: {}".format(serializer.errors)
        )
        instance = serializer.save()
        for key, value in BASE_STATION_TYPE_DESERIALIZER_DATA.items():
            self.assertEqual(
                getattr(instance, key), value,
                msg=f"The deserialized data does not match the expected data for field '{key}'."
            )

class ServiceInStationSerializerTestCase(APITestCase):
    """
    Test case for the ServiceInStationSerializer.
    """

    fixtures = ['user', 'economy', 'system', 'body', 'bgs', 'station', 'station_test_data']

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the test case.
        This method is called once for the entire test case.
        """
        cls.user = User.objects.create_user(
            username=cls.__class__.__name__,
        )
        cls.station = Station.objects.first()
    
    def test_serializer(self):
        instance = ServiceInStation.objects.get(id=1)
        serializer = ServiceInStationSerializer(instance)
        data = serializer.data
        self.assertDictEqual(
            data, BASE_SERVICE_IN_STATION_SERIALIZER_DATA,
            msg="The serialized data does not match the expected data."
        )

    def test_deserializer(self):
        serializer = ServiceInStationSerializer(data=BASE_SERVICE_IN_STATION_DESERIALIZER_DATA)
        is_valid = serializer.is_valid()
        self.assertTrue(
            is_valid,
            msg="The deserialized data is not valid. Errors: {}".format(serializer.errors)
        )
        instance = serializer.save(
            created_by=self.user,
            updated_by=self.user,
            station=self.station
        )
        self.assertEqual(
            instance.service.name, BASE_SERVICE_IN_STATION_DESERIALIZER_DATA["service"],
            msg="The deserialized data does not match the expected data for field 'service'."
        )

    def test_many_deserializer(self):
        serializer = ServiceInStationSerializer(
            data=BASE_MANY_SERVICE_IN_STATION_DESERIALIZER_DATA, many=True,
            context={'station_pk': self.station.pk}
        )
        is_valid = serializer.is_valid()
        self.assertTrue(
            is_valid,
            msg="The deserialized data is not valid. Errors: {}".format(serializer.errors)
        )
        instances = serializer.save(
            created_by=self.user,
            updated_by=self.user,
            station=self.station
        )
        qs = ServiceInStation.objects.filter(station=self.station)
        for item in BASE_MANY_SERVICE_IN_STATION_DESERIALIZER_DATA:
            self.assertTrue(
                qs.filter(service__name=item['service']).exists(),
                msg=f"The deserialized data does not contain the expected service '{item['service']}' in the station."
            )
        for instance in instances:
            self.assertEqual(
                instance.station, self.station,
                msg="The deserialized data does not match the expected station."
            )
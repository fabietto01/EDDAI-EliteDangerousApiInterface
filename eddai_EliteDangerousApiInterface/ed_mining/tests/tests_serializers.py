from rest_framework.test import APITestCase

from ed_mining.models import (
    HotspotType,
    HotSpot,
    Ring
)

from ed_mining.api.serializers import (
    RingSerializer, RingDistanceSerializer,
    HotspotTypeModelSerializer,
    HotSpotInRingBasicInformation, HotSpotInRingSerializer
)
from ed_system.models import System
from users.models import User

from django.db.models import F
from django.db.models.functions import Round
from ed_core.functions import Distanza3D


BASE_RING_SERIALIZER_DATA = {
    "id": 1,
    "system": {
        "id": 11,
        "name": "Sol"
    },
    "body": {
        "id": 2,
        "name": "Earth"
    },
    "hotSpot": [
        {
            "type": "Tritium",
            "count": 4
        },
        {
            "type": "Low Temperature Diamond",
            "count": 2
        }
    ],
    "created_at": "2025-05-06T16:34:38.802000Z",
    "updated_at": "2025-05-06T16:34:38.802000Z",
    "name": "Earth Ring",
    "innerRad": 151190000.0,
    "outerRad": 185070000.0,
    "massMT": 268920000000.0,
    "type": "MetalRich",
    "created_by": 1,
    "updated_by": 1
}

BASE_RING_DESERIALIZER_DATA = {
    "body_id": 1,
    "name": "Sol Ring",
    "innerRad": 151190000.0,
    "outerRad": 185070000.0,
    "massMT": 268920000000.0,
    "type": "MetalRich",
}

BASE_HOTSPOT_TYPE_SERIALIZER_DATA = {
    "id": 14,
    "name": "Tritium"
}

BASE_HOTSPOT_TYPE_DESERIALIZER_DATA = {
    "name": "Test Hotspot Type"
}

class RingSerializerTestCase(APITestCase):

    fixtures = ['user', 'economy', 'system', 'body', 'mining', 'body_test_data', 'ring_test_data']

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
        instance = Ring.objects.get(id=1)
        serializer = RingSerializer(instance)
        data = serializer.data
        self.assertDictEqual(
            data, BASE_RING_SERIALIZER_DATA,
            msg="The serialized data does not match the expected data."
        )

    def test_deserializer(self):
        serializer = RingSerializer(data=BASE_RING_DESERIALIZER_DATA)
        is_valid = serializer.is_valid()
        self.assertTrue(
            is_valid,
            msg="The deserialized data is not valid. Errors: {}".format(serializer.errors)
        )
        instance = serializer.save(
            created_by=self.user,
            updated_by=self.user
        )
        for key, value in BASE_RING_DESERIALIZER_DATA.items():
            if not key in ['body_id', 'type' ]:
                self.assertEqual(
                    getattr(instance, key), value,
                    msg=f"The deserialized data does not match the expected data for field '{key}'."
                )
        self.assertEqual(
            instance.ringType, BASE_RING_DESERIALIZER_DATA["type"],
            msg="The deserialized data does not match the expected data for field 'type'."
        )
        self.assertEqual(
            instance.body.id, BASE_RING_DESERIALIZER_DATA["body_id"],
            msg="The deserialized data does not match the expected data for field 'body_id'."
        )

    def test_many_serializer(self):
        qs = Ring.objects.all()
        serializer = RingSerializer(qs, many=True)
        data = serializer.data
        self.assertEqual(
            len(data), 2,
            msg="The serialized data does not match the expected data."
        )
        
class RingDistanceSerializerTestCase(APITestCase):
    """
    Test case for the RingDistanceSerializer.
    """

    fixtures = ['user', 'economy', 'system', 'body', 'mining', 'body_test_data', 'ring_test_data']

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the test case.
        This method is called once for the entire test case.
        """
        cls.sytem = System.objects.first()

    def test_distance_serializer(self):
        qs = Ring.objects.all().annotate(
            distance_st=Round(
                Distanza3D(
                    F('body__system__coordinate'),
                    point=self.sytem.coordinate
                ),
                3
            )
        )
        serializer = RingDistanceSerializer(qs, many=True)
        data = serializer.data
        self.assertEqual(
            len(data), 2,
            msg="The serialized data does not match the expected data."
        )
        for item in data:
            self.assertIn('distance_st', item, msg="The 'distance_st' field is missing in the serialized data.")
            distance_calculated = System.get_distance(
                self.sytem,
                System.objects.get(id=item['system']['id'])
            )
            self.assertEqual(
                item['distance_st'], distance_calculated,
                msg="The 'distance_st' field does not match the expected value."
            )

class HotspotTypeSerializerTestCase(APITestCase):

    fixtures = ['user', 'economy', 'system', 'body', 'mining', 'body_test_data', 'ring_test_data']

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
        instance = HotspotType.objects.get(id=14)
        serializer = HotspotTypeModelSerializer(instance)
        data = serializer.data
        self.assertDictEqual(
            data, BASE_HOTSPOT_TYPE_SERIALIZER_DATA,
            msg="The serialized data does not match the expected data."
        )

    def test_deserializer(self):
        serializer = HotspotTypeModelSerializer(data=BASE_HOTSPOT_TYPE_DESERIALIZER_DATA)
        is_valid = serializer.is_valid()
        self.assertTrue(
            is_valid,
            msg="The deserialized data is not valid. Errors: {}".format(serializer.errors)
        )
        instance = serializer.save()
        for kay, value in BASE_HOTSPOT_TYPE_DESERIALIZER_DATA.items():
            self.assertEqual(
                getattr(instance, kay), value,
                msg=f"The deserialized data does not match the expected data for field '{kay}'."
            )

class HotSpotInRingSerializerTestCase(APITestCase):
    """
    Test case for the HotSpotInRingBasicInformation serializer.
    """

    fixtures = ['user', 'economy', 'system', 'body', 'mining', 'body_test_data', 'ring_test_data']

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
        instance = HotSpot.objects.get(id=1)
        serializer = HotSpotInRingBasicInformation(instance)
        data = serializer.data
        self.assertDictEqual(
            data, {
                "type": "Tritium",
                "count": 4
            },
            msg="The serialized data does not match the expected data."
        )

    def test_deserializer(self):
        data = {
            "type_id": 8,
            "count": 2
        }
        serializer = HotSpotInRingBasicInformation(data=data)
        is_valid = serializer.is_valid()
        self.assertTrue(
            is_valid,
            msg="The deserialized data is not valid. Errors: {}".format(serializer.errors)
        )
        instance = serializer.save(
            created_by=self.user,
            updated_by=self.user,
            ring=Ring.objects.first()
        )
        self.assertEqual(
            instance.type.id, data["type_id"],
            msg="The deserialized data does not match the expected data for field 'type_id'."
        )
        self.assertEqual(
            instance.count, data["count"],
            msg="The deserialized data does not match the expected data for field 'count'."
        )
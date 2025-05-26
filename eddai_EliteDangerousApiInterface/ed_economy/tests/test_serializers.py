from django.test import TestCase
from django.db.utils import IntegrityError

from ed_economy.models import (
    Commodity, Economy,
    CommodityInStation
)

from ed_economy.api.serializers import (
    CompactedCommoditySerializer, CommoditySerializer,
    EconomyBasicInformationSerializer, EconomySerializer,
    CommodityInStationSerializer
)

from users.models import User

class CommoditySerializerTestCase(TestCase):
    """
    Test case for testing the Commodity serializers and deserializers.
    This test case includes the following tests:
    1. `test_compacted_serializer`: Verifies that the `CompactedCommoditySerializer` correctly serializes a `Commodity` instance into a compact representation containing only the `id` and `name` fields.
    2. `test_compacted_deserializer`: Verifies that the `CompactedCommoditySerializer` correctly deserializes data into a `Commodity` instance and ensures the fields match the input data.
    3. `test_serializer`: Verifies that the `CommoditySerializer` correctly serializes a `Commodity` instance into a detailed representation containing `id`, `name`, `description`, and `meanPrice` fields.
    4. `test_deserializer`: Verifies that the `CommoditySerializer` correctly deserializes data into a `Commodity` instance and ensures the fields match the input data.
    Fixtures:
    - `user`: Preloaded user data for testing.
    - `economy`: Preloaded economy data for testing.
    Assertions:
    - Ensures that the serialized data matches the expected output.
    - Ensures that the deserialized instance fields match the input data.
    - Validates the serializer's `is_valid` method and checks for errors if validation fails.
    """


    fixtures = ['user', 'economy',]

    def test_compacted_serializer(self):
        instance = Commodity.objects.get(name="Advanced Medicines")
        serializer = CompactedCommoditySerializer(
            instance
        )
        self.assertEqual(
            serializer.data,
            {
                'id': instance.id,
                'name': instance.name,
            }
        )
    
    def test_compacted_deserializer(self):
        data = {
            'name': "Test",
        }
        serielizer = CompactedCommoditySerializer(data=data)
        is_valid = serielizer.is_valid()
        self.assertTrue(is_valid, serielizer.errors)
        with self.assertRaises(IntegrityError):
            serielizer.save()

    def test_serializer(self):
        instance = Commodity.objects.get(name="Advanced Medicines")
        serializer = CommoditySerializer(
            instance
        )
        self.assertEqual(
            serializer.data,
            {
                'id': instance.id,
                'name': instance.name,
                'description': instance.description,
                'meanPrice': instance.meanPrice,
            }
        )

    def test_deserializer(self):
        data = {
            'name': "Test",
            'description': "Test",
            'meanPrice': 123,
        }
        serializer = CommoditySerializer(data=data)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid, serializer.errors)
        instance = serializer.save()
        for key, value in data.items():
            self.assertEqual(
                getattr(instance, key), value,
                f"Error in {key} field"
            )

class EconomySerializerTestCase(TestCase):
    """
    Test case for testing the Economy serializers and deserializers.
    This test case includes the following tests:
    1. `test_compacted_serializer`: Verifies that the `CompactedEconomySerializer` correctly serializes an `Economy` instance into a compact representation containing only the `id` and `name` fields.
    2. `test_compacted_deserializer`: Verifies that the `CompactedEconomySerializer` correctly deserializes data into an `Economy` instance and ensures the fields match the input data.
    3. `test_serializer`: Verifies that the `EconomySerializer` correctly serializes an `Economy` instance into a detailed representation containing all fields.
    4. `test_deserializer`: Verifies that the `EconomySerializer` correctly deserializes data into an `Economy` instance and ensures the fields match the input data.
    Fixtures:
    - `user`: Preloaded user data for testing.
    - `economy`: Preloaded economy data for testing.
    Assertions:
    - Ensures that the serialized data matches the expected output.
    - Ensures that the deserialized instance fields match the input data.
    - Validates the serializer's `is_valid` method and checks for errors if validation fails.
    """
    fixtures = ['user', 'economy',]

    def test_compacted_serializer(self):
        instance = Economy.objects.get(name="Agriculture")
        serializer = EconomyBasicInformationSerializer(
            instance
        )
        self.assertEqual(
            serializer.data,
            {
                'id': instance.id,
                'name': instance.name,
            }
        )

    def test_compacted_deserializer(self):
        data = {
            'name': "Test",
        }
        serializer = EconomyBasicInformationSerializer(data=data)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid, serializer.errors)
        instance = serializer.save()
        for key, value in data.items():
            self.assertEqual(
                getattr(instance, key), value,
                f"Error in {key} field"
            )

    def test_serializer(self):
        instance = Economy.objects.get(name="Agriculture")
        serializer = EconomySerializer(
            instance
        )
        self.assertEqual(
            serializer.data,
            {
                'id': instance.id,
                'name': instance.name,
                'description': instance.description,
            }
        )

    def test_deserializer(self):
        data = {
            'name': "Test",
            'description': "Test",
        }
        serializer = EconomySerializer(data=data)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid, serializer.errors)
        instance = serializer.save()
        for key, value in data.items():
            self.assertEqual(
                getattr(instance, key), value,
                f"Error in {key} field"
            )

class CommodityInStationSerializerTestCase(TestCase):

    fixtures = ['user', 'economy', 'system', 'station', 'bgs', 'economy_test_data']

    @classmethod
    def setUpTestData(cls):
        cls.instance_user = User.objects.create_user(
            username='testuser'
        )

    def test_serializer(self):
        instance = CommodityInStation.objects.first()
        serializer = CommodityInStationSerializer(
            instance
        )
        self.assertEqual(
            serializer.data['commodity'],
            instance.commodity.name,
            f"Error in commodity field"
        )
        self.assertEqual(
            serializer.data['buyPrice'],
            instance.buyPrice,
            f"Error in buyPrice field"
        )
        self.assertEqual(
            serializer.data['sellPrice'],
            instance.sellPrice,
            f"Error in sellPrice field"
        )
        self.assertEqual(
            serializer.data['inStock'],
            instance.inStock,
            f"Error in inStock field"
        )
        self.assertEqual(
            serializer.data['stockBracket'],
            instance.stockBracket,
            f"Error in stockBracket field"
        )
        self.assertEqual(
            serializer.data['demand'],
            instance.demand,
            f"Error in demand field"
        )
        self.assertEqual(
            serializer.data['demandBracket'],
            instance.demandBracket,
            f"Error in demandBracket field"
        )
        self.assertTrue(
            serializer.data['created_at'],
            f"Error in created_at field"
        )
        self.assertTrue(
            serializer.data['updated_at'],
            f"Error in updated_at field"
        )
        self.assertTrue(
            serializer.data['created_by'],
            f"Error in created_by field"
        )
        self.assertTrue(
            serializer.data['updated_by'],
            f"Error in updated_by field"
        )

    def test_deserializer(self):
        data = {
            'commodity': 'Algae',
            'buyPrice': 123,
            'sellPrice': 123,
            'inStock': 123,
            'stockBracket': 123,
            'demand': 123.0,
            'demandBracket': 123,
        }
        serializer = CommodityInStationSerializer(
            data=data, context={
                'station': 914,
            }
        )
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid, serializer.errors)
        instance = serializer.save(
            station_id=914,
            created_by=self.instance_user,
            updated_by=self.instance_user,
        )
        self.assertEqual(
            data.pop('commodity'),
            instance.commodity.name,
        )
        for key, value in data.items():
            self.assertEqual(
                getattr(instance, key), value,
                f"Error in {key} field"
            )

    def test_list_deserializer(self):
        data = [
            {
                'commodity': 'Agri-Medicines',
                'buyPrice': 123,
                'sellPrice': 123,
                'inStock': 123,
                'stockBracket': 123,
                'demand': 123.0,
                'demandBracket': 123,
            },
            {
                'commodity': 'Agronomic Treatment',
                'buyPrice': 123,
                'sellPrice': 123,
                'inStock': 123,
                'stockBracket': 123,
                'demand': 123.0,
                'demandBracket': 123,
            }
        ]
        serializer = CommodityInStationSerializer(
            data=data, context={
                'station_pk': 914
            },
            many=True
        )
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid, serializer.errors)
        instance = serializer.save(
            station_id=914,
            created_by=self.instance_user,
            updated_by=self.instance_user,
        )
        for i in range(len(data)):
            self.assertEqual(
                data[i].pop('commodity'),
                instance[i].commodity.name
            )
            for key, value in data[i].items():
                self.assertEqual(
                    getattr(instance[i], key), value,
                    f"Error in {key} field"
                )
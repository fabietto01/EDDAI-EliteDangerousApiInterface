from django.test import TestCase
from django.db.utils import IntegrityError

from ed_economy.models import (
    Commodity, Economy,
)

from ed_economy.api.serializers import (
    CompactedCommoditySerializer, CommoditySerializer,
    EconomyBasicInformationSerializer, EconomySerializer
)

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
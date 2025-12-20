from django.test import TestCase

from ed_material.models import MaterialInPlanet, Material

from ed_material.api.serializers import (
    CompactedMaterialSerializer, MaterialSerializer, BaseMaterialSerializer,
    CompactedMaterialInPlanetSerializer, MaterialInPlanetSerializer
)

from ed_body.models import Planet
from ed_system.models import System
from users.models import User


class MaterialSerializerTestCase(TestCase):
    """
    Test case for testing the Material model serializer.
    
    Classes:
        MaterialSerializerTestCase: Test case for testing the Material model serializer.
    
    Methods:
        test_compacted_serializer(self):
            Tests the CompactedMaterialSerializer serializer.
        test_compacted_deserializer(self):
            Tests the CompactedMaterialSerializer deserializer.
        test_base_serializer(self):
            Tests the BaseMaterialSerializer serializer.
        test_base_deserializer(self):
            Tests the BaseMaterialSerializer deserializer.
        test_serializer(self):
            Tests the MaterialSerializer serializer.
        test_deserializer(self):
            Tests the MaterialSerializer deserializer.
    """

    fixtures = ['user', 'economy', 'system', 'body', 'material']

    @classmethod
    def setUpTestData(cls):
        cls.instance_material = Material.objects.get(id=1)

    def test_compacted_serializer(self):
        serializer = CompactedMaterialSerializer(
            instance=self.instance_material
        )
        data = {
            'id': self.instance_material.id,
            'name': self.instance_material.name
        }
        self.assertEqual(serializer.data, data)

    def test_compacted_deserializer(self):
        data = {
            'name': 'test_compacted_deserializer',
        }
        serializer = CompactedMaterialSerializer(data=data)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid, msg=serializer.errors)
        instance = serializer.save(
            type=Material.MaterialType.RAW,
            grade=Material.MaterialGrade.COMMON
        )
        self.assertEqual(instance.name, data.get('name'))
        self.assertEqual(instance.type, Material.MaterialType.RAW)
        self.assertEqual(instance.grade, Material.MaterialGrade.COMMON)

    def test_base_serializer(self):
        serializer = BaseMaterialSerializer(
            instance=self.instance_material
        )
        data = {
            'id': self.instance_material.id,
            'name': self.instance_material.name,
            'type': self.instance_material.type,
            'grade': self.instance_material.grade
        }
        self.assertEqual(serializer.data, data)

    def test_base_deserializer(self):
        data = {
            'name': 'test_base_deserializer',
            'type': Material.MaterialType.MANUFACTURED,
            'grade': Material.MaterialGrade.RARE
        }
        serializer = BaseMaterialSerializer(data=data)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid, msg=serializer.errors)
        instance = serializer.save()
        self.assertEqual(instance.name, data.get('name'))
        self.assertEqual(instance.type, data.get('type'))
        self.assertEqual(instance.grade, data.get('grade'))

    def test_serializer(self):
        serializer = MaterialSerializer(
            instance=self.instance_material
        )
        data = {
            'id': self.instance_material.id,
            'name': self.instance_material.name,
            'type': self.instance_material.type,
            'grade': self.instance_material.grade,
            'note': self.instance_material.note
        }
        self.assertEqual(serializer.data, data)

    def test_deserializer(self):
        data = {
            'name': 'test_deserializer',
            'type': Material.MaterialType.ENCODED,
            'grade': Material.MaterialGrade.VER_RARE
        }
        serializer = MaterialSerializer(data=data)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid, msg=serializer.errors)
        instance = serializer.save()
        self.assertEqual(instance.name, data.get('name'))
        self.assertEqual(instance.type, data.get('type'))
        self.assertEqual(instance.grade, data.get('grade'))
        self.assertEqual(instance.note, None)


class MaterialInPlanetSerializerTestCase(TestCase):
    """
    Test case for testing the MaterialInPlanet model serializer.
    
    Classes:
        MaterialInPlanetSerializerTestCase: Test case for testing the MaterialInPlanet model serializer.
    
    Methods:
        test_compacted_serializer(self):
            Tests the CompactedMaterialInPlanetSerializer serializer.
        test_validator(self):
            Tests the validator of the CompactedMaterialInPlanetSerializer serializer.
        test_compacted_deserializer(self):
            Tests the CompactedMaterialInPlanetSerializer deserializer.
        test_serializer(self):
            Tests the MaterialInPlanetSerializer serializer.
        test_deserializer(self):
            Tests the MaterialInPlanetSerializer deserializer.
        test_list_deserializer(self):
            Tests the MaterialInPlanetSerializer deserializer for a list of instances.
    """

    fixtures = ['user', 'economy', 'system', 'body', 'material']

    @classmethod
    def setUpTestData(cls):
        cls.instance_user = User.objects.create_user(
            username="MaterialInPlanetSerializerTestCase_user",
        )
        cls.istance_system = System.objects.get(name="Sol")
        cls.instance_planet = Planet.objects.create(
            name="MaterialInPlanetSerializerTestCase_planet",
            system=cls.istance_system,
            bodyID=100,
            created_by=cls.instance_user,
            updated_by=cls.instance_user
        )
        cls.instance_material_raw = Material.objects.get(id=1)  # RAW material from fixture
        cls.instance_material_raw_2 = Material.objects.get(id=2)  # Another RAW material from fixture
        cls.instance_material_manufactured = Material.objects.create(
            name="MaterialInPlanetSerializerTestCase_manufactured",
            type=Material.MaterialType.MANUFACTURED,
            grade=Material.MaterialGrade.RARE
        )
        cls.instance_material_in_planet = MaterialInPlanet.objects.create(
            planet=cls.instance_planet,
            material=cls.instance_material_raw,
            percent=45.5,
            created_by=cls.instance_user,
            updated_by=cls.instance_user
        )

    def test_compacted_serializer(self):
        serializer = CompactedMaterialInPlanetSerializer(
            instance=self.instance_material_in_planet
        )
        data = {
            'id': self.instance_material_in_planet.id,
            'material': {
                'id': self.instance_material_raw.id,
                'name': self.instance_material_raw.name
            },
            'percent': self.instance_material_in_planet.percent
        }
        self.assertEqual(serializer.data, data)

    def test_validator(self):
        data = {
            'material_id': self.instance_material_manufactured.id,
            'percent': 50.0
        }
        serializer = MaterialInPlanetSerializer(
            data=data
        )
        is_valid = serializer.is_valid()
        self.assertFalse(is_valid)
        self.assertIn('material_id', serializer.errors)

    def test_compacted_deserializer(self):
        # CompactedMaterialInPlanetSerializer is read-only, so this test is not applicable
        pass

    def test_serializer(self):
        serializer = MaterialInPlanetSerializer(
            instance=self.instance_material_in_planet
        )
        data = {
            'id': self.instance_material_in_planet.id,
            'material': {
                'id': self.instance_material_raw.id,
                'name': self.instance_material_raw.name
            },
            'percent': self.instance_material_in_planet.percent,
            'created_at': self.instance_material_in_planet.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'updated_at': self.instance_material_in_planet.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'created_by': self.instance_material_in_planet.created_by.id,
            'updated_by': self.instance_material_in_planet.updated_by.id
        }
        self.assertEqual(serializer.data, data)

    def test_deserializer(self):
        data = {
            'material_id': self.instance_material_raw_2.id,
            'percent': 30.5
        }
        serializer = MaterialInPlanetSerializer(
            data=data
        )
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid, msg=serializer.errors)
        instance = serializer.save(
            planet=self.instance_planet,
            created_by=self.instance_user,
            updated_by=self.instance_user
        )
        self.assertEqual(instance.material, self.instance_material_raw_2)
        self.assertEqual(instance.percent, data.get('percent'))
        self.assertEqual(instance.planet, self.instance_planet)
        self.assertEqual(instance.created_by, self.instance_user)
        self.assertEqual(instance.updated_by, self.instance_user)

    def test_list_deserializer(self):
        instance_planet = Planet.objects.create(
            name="test_list_deserializer_planet",
            system=self.istance_system,
            bodyID=101,
            created_by=self.instance_user,
            updated_by=self.instance_user
        )
        material_3 = Material.objects.get(id=3)  # Another RAW material from fixture
        material_4 = Material.objects.get(id=4)  # Another RAW material from fixture
        
        data = [
            {
                'material_id': material_3.id,
                'percent': 25.0
            },
            {
                'material_id': material_4.id,
                'percent': 35.0
            }
        ]
        serializer = MaterialInPlanetSerializer(
            data=data, many=True
        )
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid, msg=serializer.errors)
        instances = serializer.save(
            planet=instance_planet,
            created_by=self.instance_user,
            updated_by=self.instance_user
        )
        self.assertEqual(len(instances), 2)
        self.assertEqual(instances[0].material, material_3)
        self.assertEqual(instances[0].percent, data[0].get('percent'))
        self.assertEqual(instances[0].planet, instance_planet)
        self.assertEqual(instances[0].created_by, self.instance_user)
        self.assertEqual(instances[0].updated_by, self.instance_user)
        self.assertEqual(instances[1].material, material_4)
        self.assertEqual(instances[1].percent, data[1].get('percent'))
        self.assertEqual(instances[1].planet, instance_planet)
        self.assertEqual(instances[1].created_by, self.instance_user)
        self.assertEqual(instances[1].updated_by, self.instance_user)
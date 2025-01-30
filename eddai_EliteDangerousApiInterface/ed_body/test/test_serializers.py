from django.test import TestCase

from ed_body.models import (
    AtmosphereComponent, AtmosphereComponentInPlanet,
    Planet, Volcanism,
    AtmosphereType,
    StarLuminosity,
    StarType,
    BaseBody
)
from ed_body.api.serializers import (
    CompactedAtmosphereComponentSerializer, AtmosphereComponentSerializer,
    CompactedAtmosphereComponentInPlanetSerializer, AtmosphereComponentInPlanetSerializer,
    CompactedAtmosphereTypeSerializer, AtmosphereTypeSerializer,
    PlanetTypeSerializer, CompactedPlanetTypeSerializer,
    VolcanismSerializer, CompactedVolcanismSerializer,
    StarLuminositySerializer, CompactedStarLuminositySerializer,
    StarTypeSerializer, CompactedStarTypeSerializer,
    BaseBodySerializer, BaseBodyDistanceSerializer
)
from ed_system.models import System
from users.models import User

class AtmosphereComponentSerializerTestCase(TestCase):
    """
    Test case for testing the AtmosphereComponent model serializer.
    Classes:
        CompactedAtmosphereComponentSerializerTestCase: Test case for testing the AtmosphereComponent model serializer.
    Methods:
        test_compacted_serializer(self):
            Tests the CompactedAtmosphereComponentSerializer serializer.
        test_compacted_deserializer(self):
            Tests the CompactedAtmosphereComponentSerializer deserializer.
        test_serializer(self):
            Tests the AtmosphereComponentSerializer serializer.
        test_deserializer(self):
            Tests the AtmosphereComponentSerializer deserializer.
    """

    fixtures = ['user', 'economy', 'system', 'body']

    def test_compacted_serializer(self):
        instance = AtmosphereComponent.objects.get(name="Nitrogen")
        serializer = CompactedAtmosphereComponentSerializer(
            instance=instance
        )
        self.assertEqual(serializer.data, {'id': instance.id, 'name': instance.name})   

    def test_compacted_deserializer(self):
        data = {'name': 'test_deserializer'}
        serializer = CompactedAtmosphereComponentSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEqual(instance.name, data.get('name'))

    def test_serializer(self):
        instance = AtmosphereComponent.objects.get(name="Nitrogen")
        serializer = AtmosphereComponentSerializer(
            instance=instance
        )
        data = {
            'id': instance.id, 'name': instance.name,
            'note': instance.note
        }
        self.assertEqual(serializer.data, data)

    def test_deserializer(self):
        data = {'name': 'test_deserializer'}
        serializer = AtmosphereComponentSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEqual(instance.name, data.get('name'))
        self.assertEqual(instance.note, None)

class AtmosphereComponentInPlanetSerializerTestCase(TestCase):
    """
    Test case for testing the AtmosphereComponentInPlanet model serializer.
    Classes:
        CompactedAtmosphereComponentInPlanetSerializerTestCase: Test case for testing the AtmosphereComponentInPlanet model serializer.
    Methods:
        test_compacted_serializer(self):
            Tests the CompactedAtmosphereComponentInPlanetSerializer serializer.
        test_validator(self):
            Tests the validator of the CompactedAtmosphereComponentInPlanetSerializer serializer.
        test_compacted_deserializer(self):
            Tests the CompactedAtmosphereComponentInPlanetSerializer deserializer.
        test_serializer(self):
            Tests the AtmosphereComponentInPlanetSerializer serializer.
        test_deserializer(self):
            Tests the AtmosphereComponentInPlanetSerializer deserializer.
        test_list_deserializer(self):
            Tests the AtmosphereComponentInPlanetSerializer deserializer for a list of instances.
    """

    fixtures = ['user', 'economy', 'system', 'body']

    @classmethod
    def setUpTestData(cls):
        cls.instance_user = User.objects.create_user(
            username="AtmosphereComponentInPlanetSerializerTestCase_user",
        )
        cls.istance_system = System.objects.get(name="Sol")
        cls.instance_planet = Planet.objects.create(
            name = "AtmosphereComponentInPlanetSerializerTestCase_planet",
            system = cls.istance_system,
            bodyID = 2,
            created_by=cls.instance_user,
            updated_by=cls.instance_user
        )
        cls.instance_atmosphere_component = AtmosphereComponent.objects.get(id=1)
        cls.instance_atmosphere_component_2 = AtmosphereComponent.objects.get(id=2)
        cls.instance_atmosphere_in_planet = AtmosphereComponentInPlanet.objects.create(
            planet=cls.instance_planet, atmosphere_component=cls.instance_atmosphere_component, percent=78.0,
            created_by=cls.instance_user, updated_by=cls.instance_user
        )

    def test_compacted_serializer(self):
        serializer = CompactedAtmosphereComponentInPlanetSerializer(
            instance=self.instance_atmosphere_in_planet
        )
        data = {
            'atmosphere': self.instance_atmosphere_component.name,
            'percent': self.instance_atmosphere_in_planet.percent
        }
        self.assertEqual(serializer.data, data)

    def test_validator(self):
        data = {
            'atmosphere': self.instance_atmosphere_component.name,
            'percent': 100
        }
        serializer = CompactedAtmosphereComponentInPlanetSerializer(
            data=data
        )
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors, {'non_field_errors': ['An internal server error occurred']})
        serializer = CompactedAtmosphereComponentInPlanetSerializer(
            data=data, context={'planet_pk': self.instance_planet.pk}
        )
        self.assertFalse(serializer.is_valid())
        self.assertEqual(serializer.errors, {'non_field_errors': ['the sum of the percent for the planet cannot be greater than 100']})
        data['percent'] = 22.0
        serializer = CompactedAtmosphereComponentInPlanetSerializer(
            data=data, context={'planet_pk': self.instance_planet.pk}
        )
        self.assertTrue(serializer.is_valid())

    def test_compacted_deserializer(self):
        data = {
            'atmosphere': self.instance_atmosphere_component_2.name,
            'percent': 22.0
        }
        serializer = CompactedAtmosphereComponentInPlanetSerializer(
            data=data, context={'planet_pk': self.instance_planet.pk}
        )
        self.assertTrue(serializer.is_valid())
        instance = serializer.save(
            planet=self.instance_planet,
            created_by=self.instance_user,
            updated_by=self.instance_user
        )
        self.assertEqual(instance.atmosphere_component.name, data.get('atmosphere'))
        self.assertEqual(instance.percent, data.get('percent'))

    def test_serializer(self):
        serializer = AtmosphereComponentInPlanetSerializer(
            instance=self.instance_atmosphere_in_planet
        )
        data = {
            'id': self.instance_atmosphere_in_planet.id,
            'atmosphere': self.instance_atmosphere_component.name,
            'created_at': self.instance_atmosphere_in_planet.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'updated_at': self.instance_atmosphere_in_planet.updated_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            'percent': self.instance_atmosphere_in_planet.percent,
            'created_by': self.instance_atmosphere_in_planet.created_by.id,
            'updated_by': self.instance_atmosphere_in_planet.updated_by.id
        }
        self.assertEqual(serializer.data, data)
    
    def test_deserializer(self):
        data = {
            'atmosphere': self.instance_atmosphere_component_2.name,
            'percent': 22.0
        }
        serializer = AtmosphereComponentInPlanetSerializer(
            data=data, context={'planet_pk': self.instance_planet.pk}
        )
        self.assertTrue(serializer.is_valid())
        instance:AtmosphereComponentInPlanetSerializer = serializer.save(
            planet=self.instance_planet,
            created_by=self.instance_user,
            updated_by=self.instance_user
        )
        self.assertEqual(instance.atmosphere_component.name, data.get('atmosphere'))
        self.assertEqual(instance.percent, data.get('percent'))
        self.assertEqual(instance.planet, self.instance_planet)
        self.assertEqual(instance.created_by, self.instance_user)
        self.assertEqual(instance.updated_by, self.instance_user)

    def test_list_deserializer(self):
        instance_planet = Planet.objects.create(
            name = "test_list_deserializer_planet",
            system = self.istance_system,
            bodyID = 3,
            created_by=self.instance_user,
            updated_by=self.instance_user
        )
        data = [
            {
                'atmosphere': self.instance_atmosphere_component.name,
                'percent': 22.0
            },
            {
                'atmosphere': self.instance_atmosphere_component_2.name,
                'percent': 22.0
            }
        ]
        serializer = AtmosphereComponentInPlanetSerializer(
            data=data, context={'planet_pk': instance_planet.pk}, many=True
        )
        self.assertTrue(serializer.is_valid())
        instances = serializer.save(
            planet=instance_planet,
            created_by=self.instance_user,
            updated_by=self.instance_user
        )
        self.assertEqual(len(instances), 2)
        self.assertEqual(instances[0].atmosphere_component.name, data[0].get('atmosphere'))
        self.assertEqual(instances[0].percent, data[0].get('percent'))
        self.assertEqual(instances[0].planet, instance_planet)
        self.assertEqual(instances[0].created_by, self.instance_user)
        self.assertEqual(instances[0].updated_by, self.instance_user)
        self.assertEqual(instances[1].atmosphere_component.name, data[1].get('atmosphere'))
        self.assertEqual(instances[1].percent, data[1].get('percent'))
        self.assertEqual(instances[1].planet, instance_planet)
        self.assertEqual(instances[1].created_by, self.instance_user)
        self.assertEqual(instances[1].updated_by, self.instance_user)

class AtmosphereTypeSerializerTestCase(TestCase):
    """
    Test case for testing the AtmosphereType model serializer.
    Classes:
        AtmosphereTypeSerializerTestCase: Test case for testing the AtmosphereType model serializer.
    Methods:
        test_compacted_serializer(self):
            Tests the CompactedAtmosphereTypeSerializer serializer.
        
    """

    fixtures = ['user', 'economy', 'system', 'body']

    @classmethod
    def setUpTestData(cls):
        cls.instance_atmosphereType = AtmosphereType.objects.get(id=1)

    def test_compacted_serializer(self):
        serializer = CompactedAtmosphereTypeSerializer(
            instance=self.instance_atmosphereType
        )
        data = {
            'id': self.instance_atmosphereType.id,
            'name': self.instance_atmosphereType.name
        }
        self.assertEqual(serializer.data, data)

    def test_compacted_deserializer(self):
        data = {
            'name': 'test_compacted_deserializer'
        }
        serializer = CompactedAtmosphereTypeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEqual(instance.name, data.get('name'))

    def test_serializer(self):
        serializer = AtmosphereTypeSerializer(
            instance=self.instance_atmosphereType
        )
        data = {
            'id': self.instance_atmosphereType.id,
            'name': self.instance_atmosphereType.name,
            'note': self.instance_atmosphereType.note
        }
        self.assertEqual(serializer.data, data)

    def test_deserializer(self):
        data = {
            'name': 'test_deserializer'
        }
        serializer = AtmosphereTypeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEqual(instance.name, data.get('name'))
        self.assertEqual(instance.note, None)

class PlanetTypeSerializerTestCase(TestCase):
    """
    Test case for testing the PlanetType model serializer.
    Classes:
        PlanetTypeSerializerTestCase: Test case for testing the PlanetType model serializer.
    Methods:
        test_compacted_serializer(self):
            Tests the CompactedPlanetTypeSerializer serializer.
        test_compacted_deserializer(self):
            Tests the CompactedPlanetTypeSerializer deserializer.
        test_serializer(self):
            Tests the PlanetTypeSerializer serializer.
        test_deserializer(self):
            Tests the PlanetTypeSerializer deserializer.
    """

    fixtures = ['user', 'economy', 'system', 'body']

    @classmethod
    def setUpTestData(cls):
        cls.instance_planetType = AtmosphereType.objects.get(id=1)

    def test_compacted_serializer(self):
        serializer = CompactedPlanetTypeSerializer(
            instance=self.instance_planetType
        )
        data = {
            'id': self.instance_planetType.id,
            'name': self.instance_planetType.name
        }
        self.assertEqual(serializer.data, data)
    
    def test_compacted_deserializer(self):
        data = {
            'name': 'test_compacted_deserializer'
        }
        serializer = CompactedPlanetTypeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEqual(instance.name, data.get('name'))

    def test_serializer(self):
        serializer = PlanetTypeSerializer(
            instance=self.instance_planetType
        )
        data = {
            'id': self.instance_planetType.id,
            'name': self.instance_planetType.name,
            'note': self.instance_planetType.note
        }
        self.assertEqual(serializer.data, data)

    def test_deserializer(self):
        data = {
            'name': 'test_deserializer'
        }
        serializer = PlanetTypeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEqual(instance.name, data.get('name'))
        self.assertEqual(instance.note, None)

class VolcanismSerializerTestCase(TestCase):
    """
    Test case for testing the Volcanism model serializer.
    Classes:
        VolcanismSerializerTestCase: Test case for testing the Volcanism model serializer.
    Methods:
        test_compacted_serializer(self):
            Tests the CompactedVolcanismSerializer serializer.
        test_compacted_deserializer(self):
            Tests the CompactedVolcanismSerializer deserializer.
        test_serializer(self):
            Tests the VolcanismSerializer serializer.
        test_deserializer(self):
            Tests the VolcanismSerializer deserializer.
    """

    fixtures = ['user', 'economy', 'system', 'body']

    @classmethod
    def setUpTestData(cls):
        cls.instance_volcanism = Volcanism.objects.get(id=1)

    def test_compacted_serializer(self):
        serializer = CompactedVolcanismSerializer(
            instance=self.instance_volcanism
        )
        data = {
            'id': self.instance_volcanism.id,
            'name': self.instance_volcanism.name
        }
        self.assertEqual(serializer.data, data)

    def test_compacted_deserializer(self):
        data = {
            'name': 'test_compacted_deserializer'
        }
        serializer = CompactedVolcanismSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEqual(instance.name, data.get('name'))

    def test_serializer(self):
        serializer = VolcanismSerializer(
            instance=self.instance_volcanism
        )
        data = {
            'id': self.instance_volcanism.id,
            'name': self.instance_volcanism.name,
            'note': self.instance_volcanism.note
        }
        self.assertEqual(serializer.data, data)

    def test_deserializer(self):
        data = {
            'name': 'test_deserializer'
        }
        serializer = VolcanismSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEqual(instance.name, data.get('name'))
        self.assertEqual(instance.note, None)

class StarLuminositySerializerTestCase(TestCase):
    """
    Test case for testing the StarLuminosity model serializer.
    Classes:
        StarLuminositySerializerTestCase: Test case for testing the StarLuminosity model serializer.
    Methods:
        test_compacted_serializer(self):
            Tests the CompactedStarLuminositySerializer serializer.
        test_compacted_deserializer(self):
            Tests the CompactedStarLuminositySerializer deserializer.
        test_serializer(self):
            Tests the StarLuminositySerializer serializer.
        test_deserializer(self):
            Tests the StarLuminositySerializer deserializer.
    """

    fixtures = ['user', 'economy', 'system', 'body']

    @classmethod
    def setUpTestData(cls):
        cls.instance_starLuminosity = StarLuminosity.objects.get(id=1)

    def test_compacted_serializer(self):
        serializer = CompactedStarLuminositySerializer(
            instance=self.instance_starLuminosity
        )
        data = {
            'id': self.instance_starLuminosity.id,
            'name': self.instance_starLuminosity.name
        }
        self.assertEqual(serializer.data, data)

    def test_compacted_deserializer(self):
        data = {
            'name': 'test_compacted_deserializer'
        }
        serializer = CompactedStarLuminositySerializer(data=data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEqual(instance.name, data.get('name'))

    def test_serializer(self):
        serializer = StarLuminositySerializer(
            instance=self.instance_starLuminosity
        )
        data = {
            'id': self.instance_starLuminosity.id,
            'name': self.instance_starLuminosity.name,
            'note': self.instance_starLuminosity.note
        }
        self.assertEqual(serializer.data, data)

    def test_deserializer(self):
        data = {
            'name': 'test_deserializer'
        }
        serializer = StarLuminositySerializer(data=data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEqual(instance.name, data.get('name'))
        self.assertEqual(instance.note, None)

class StarTypeSerializerTestCase(TestCase):
    """
    Test case for testing the StarType model serializer.
    Classes:
        StarTypeSerializerTestCase: Test case for testing the StarType model serializer.
    Methods:
        test_compacted_serializer(self):
            Tests the CompactedStarTypeSerializer serializer.
        test_compacted_deserializer(self):
            Tests the CompactedStarTypeSerializer deserializer.
        test_serializer(self):
            Tests the StarTypeSerializer serializer.
        test_deserializer(self):
            Tests the StarTypeSerializer deserializer.
    """

    fixtures = ['user', 'economy', 'system', 'body']

    @classmethod
    def setUpTestData(cls):
        cls.instance_starType = StarType.objects.get(id=1)

    def test_compacted_serializer(self):
        serializer = CompactedStarTypeSerializer(
            instance=self.instance_starType
        )
        data = {
            'id': self.instance_starType.id,
            'name': self.instance_starType.name
        }
        self.assertEqual(serializer.data, data)

    def test_compacted_deserializer(self):
        data = {
            'name': 'test_compacted_deserializer'
        }
        serializer = CompactedStarTypeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEqual(instance.name, data.get('name'))

    def test_serializer(self):
        serializer = StarTypeSerializer(
            instance=self.instance_starType
        )
        data = {
            'id': self.instance_starType.id,
            'name': self.instance_starType.name,
            'note': self.instance_starType.note
        }
        self.assertEqual(serializer.data, data)

    def test_deserializer(self):
        data = {
            'name': 'test_deserializer'
        }
        serializer = StarTypeSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        instance = serializer.save()
        self.assertEqual(instance.name, data.get('name'))
        self.assertEqual(instance.note, None)

class BaseBodySerializerTestCase(TestCase):

    fixtures = ['user', 'economy', 'system', 'body', 'body_test_data']

    @classmethod
    def setUpTestData(cls):
        cls.instance_user = User.objects.create_user(
            username="BaseBodySerializerTestCase_user",
        )
        cls.instance_sytsem = System.objects.get(name="Sol")
        cls.instance_base_body = BaseBody.objects.get(name="Earth")

    def test_serializer(self):
        serializer = BaseBodySerializer(
            instance=self.instance_base_body
        )
        data = {
            'id': self.instance_base_body.id,
            'system': {
                'id': self.instance_base_body.system.id,
                'name': self.instance_base_body.system.name,
            },
            'name': self.instance_base_body.name,
            'bodyID': self.instance_base_body.bodyID,
            'parentsID': self.instance_base_body.parentsID,
            'distance': self.instance_base_body.distance,
            'radius': self.instance_base_body.radius,
            'surfaceTemperature': self.instance_base_body.surfaceTemperature,
            'eccentricity': self.instance_base_body.eccentricity,
            'orbitalInclination': self.instance_base_body.orbitalInclination,
            'orbitalPeriod': self.instance_base_body.orbitalPeriod,
            'periapsis': self.instance_base_body.periapsis,
            'semiMajorAxis': self.instance_base_body.semiMajorAxis,
            'ascendingNode': self.instance_base_body.ascendingNode,
            'meanAnomaly': self.instance_base_body.meanAnomaly,
            'axialTilt': self.instance_base_body.axialTilt,
            'rotationPeriod': self.instance_base_body.rotationPeriod,
            'created_by': self.instance_base_body.created_by.id,
            'updated_by': self.instance_base_body.updated_by.id
        }
        serializer_data_keys = [key for key in serializer.data.keys()]
        for key, item in data.items():
            self.assertTrue(key in serializer_data_keys)
            self.assertEqual(serializer.data[key], item)
            serializer_data_keys.remove(key)
        self.assertEqual(len(serializer_data_keys), 0)

    def test_deserializer(self):
        data = {
            'name': 'test_deserializer',
            'system_id': self.instance_sytsem.id,
            'bodyID': 100,
        }
        serializer = BaseBodySerializer(data=data)
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid)
        instance = serializer.save(
            created_by=self.instance_user,
            updated_by=self.instance_user
        )
        self.assertEqual(instance.name, data.get('name'))
        self.assertEqual(instance.system, self.instance_sytsem)
        self.assertEqual(instance.surfaceTemperature, data.get('surfaceTemperature', None))

    def test_distance_serializer(self):

        from ed_core.functions import Distanza3D
        from django.db.models import F

        Earth = BaseBody.objects.all().annotate(
            distance_st=Distanza3D(
                F('system__coordinate'),
                point=self.instance_sytsem.coordinate
            )
        ).get(name="Earth")
        serializer = BaseBodyDistanceSerializer(
            instance=Earth
        )
        self.assertTrue('distance_st' in serializer.data.keys())
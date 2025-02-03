from django.test import TestCase
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.core.management import call_command

from ed_body.models import (
    Planet, Star, BaseBody, StarLuminosity, StarType,
    AtmosphereComponent, AtmosphereComponentInPlanet
)
from ed_system.models import System
from users.models import User

class AtmosphereComponentTestCase(TestCase):
    """
    Test case for testing the creation and relationships of the AtmosphereComponent model.
    Classes:
        AtmosphereComponentTestCase: Test case for creating and validating the AtmosphereComponent model.
    Methods:
        setUpTestData(cls):
            Sets up initial data for the test case, including creating a user.
        test_create_atmospherecomponent(self):
            Tests the creation of an AtmosphereComponent instance and validates its attributes.
    """
    
    @classmethod
    def setUpTestData(cls):
        cls.istance_user = User.objects.create_user(
            username="AtmosphereComponentTestCase_user",
        )

    def test_create_atmospherecomponent(self):
        instance = AtmosphereComponent.objects.create(
            name="test_create_atmospherecomponent",
        )
        self.assertEqual(type(instance), AtmosphereComponent)
        self.assertEqual(instance.name, "test_create_atmospherecomponent")

class AtmosphereComponentInPlanetTestCase(TestCase):
    """
    Test case for testing the creation and relationships of the AtmosphereComponentInPlanet model.
    Classes:
        AtmosphereComponentInPlanetTestCase: Test case for creating and validating the AtmosphereComponentInPlanet model.
    Methods:
        setUpTestData(cls):
            Sets up initial data for the test case, including creating a user and a planet.
        test_create_atmospherecomponentinplanet(self):
            Tests the creation of an AtmosphereComponentInPlanet instance and validates its attributes.
        test_clean_model(self):
            Tests the clean method of the AtmosphereComponentInPlanet model, which checks that the sum of 'percent' for the planet in the database does not exceed 100.
    """
    
    fixtures = ['user', 'economy', 'system', 'body', 'bgs', 'exploration', 'material', 'mining', 'station']

    @classmethod
    def setUpTestData(cls):
        cls.istance_user = User.objects.create_user(
            username="AtmosphereComponentInPlanetTestCase_user",
        )
        cls.istance_system = System.objects.get(name="Sol")
        cls.istance_planet = Planet.objects.create(
            name = "AtmosphereComponentInPlanetTestCase_planet",
            system = cls.istance_system,
            bodyID = 1,
            created_by=cls.istance_user,
            updated_by=cls.istance_user,
        )

    def test_create_atmospherecomponentinplanet(self):
        instanceAtmosphereComponent = AtmosphereComponent.objects.get(id=2)
        instance = AtmosphereComponentInPlanet.objects.create(
            planet=self.istance_planet,
            atmosphere_component=instanceAtmosphereComponent,
            percent=100,
            created_by=self.istance_user,
            updated_by=self.istance_user,
        )
        self.assertEqual(type(instance), AtmosphereComponentInPlanet)
        self.assertEqual(instance.atmosphere_component, instanceAtmosphereComponent)
        self.assertEqual(instance.planet, self.istance_planet)

class BodyTestCase(TestCase):
    """
    Test case for testing the creation and relationships of various celestial body models.
    Classes:
        BodyTestCase: Test case for creating and validating celestial body models.
    Methods:
        setUpTestData(cls):
            Sets up initial data for the test case, including creating a user and a system.
        test_create_basebody(self):
            Tests the creation of a BaseBody instance and validates its attributes.
        test_planet_creation(self):
            Tests the creation of a Planet instance and validates its attributes.
        test_star_creation(self):
            Tests the creation of a Star instance and validates its attributes.
        test_create_children_planet(self):
            Tests the creation of a BaseBody instance and a Planet instance with the same bodyID,
            and validates their attributes and relationships. Also tests that creating a Star
            instance with the same bodyID raises an exception.
    """
    
    fixtures = ['user', 'economy', 'system', 'body', 'bgs', 'exploration', 'material', 'mining', 'station']
    
    @classmethod
    def setUpTestData(cls):
        cls.istance_user = User.objects.create_user(
            username="BodyTestCase_user",
        )
        cls.istance_system = System.objects.get(name="Sol")

    def test_create_basebody(self):
        instance = BaseBody.objects.create(
            name="test_create_basebody",
            system=self.istance_system,
            bodyID=1,
            created_by=self.istance_user,
            updated_by=self.istance_user,
        )
        self.assertEqual(type(instance), BaseBody)
        self.assertEqual(instance.name, "test_create_basebody")

    def test_planet_creation(self):
        istance_Planet = Planet.objects.create(
            name = "test_planet_creation",
            system = self.istance_system,
            bodyID = 2,
            created_by=self.istance_user,
            updated_by=self.istance_user,
        )
        self.assertEqual(type(istance_Planet), Planet)
        self.assertEqual(istance_Planet.name, "test_planet_creation")

    def test_star_creation(self):
        starType = StarType.objects.get(name="A")
        starLuminosity = StarLuminosity.objects.get(name="Ia")
        istance_Star = Star.objects.create(
            name = "test_star_creation",
            system = self.istance_system,
            absoluteMagnitude = 0,
            age = 0,
            luminosity = starLuminosity,
            starType = starType,
            subclass = 0,
            stellarMass = 0,
            bodyID = 3,
            created_by=self.istance_user,
            updated_by=self.istance_user,
        )
        self.assertEqual(type(istance_Star), Star)
        self.assertEqual(istance_Star.name, "test_star_creation")

    def test_create_children_planet(self):
        instanceBaseBody = BaseBody.objects.create(
            name="test_create_children_planet",
            system=self.istance_system,
            bodyID=4,
            created_by=self.istance_user,
            updated_by=self.istance_user,
        )
        self.assertEqual(type(instanceBaseBody), BaseBody)
        self.assertEqual(instanceBaseBody.name, "test_create_children_planet")
        instancePlanet = Planet.objects.create(
            name = "test_create_children_planet",
            system=self.istance_system,
            bodyID=4,
            updated_by=self.istance_user,
        )    
        self.assertEqual(type(instancePlanet), Planet)
        self.assertEqual(instancePlanet.name, "test_create_children_planet")
        self.assertEqual(instancePlanet.basebody_ptr, instanceBaseBody) 
        with self.assertRaises(Exception):
            Star.objects.create(
                name = "test_create_children_planet",
                system=self.istance_system,
                bodyID=4,
                updated_by=self.istance_user,
            )
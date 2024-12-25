from django.test import TestCase
from django.contrib.gis.geos import Point

from ed_body.models import Planet, Star, BaseBody, StarLuminosity, StarType
from ed_system.models import System
from users.models import User

class BodyTestCase(TestCase):
    
    @classmethod
    def setUpTestData(cls):
        cls.istance_user = User.objects.create_user(
            username="test",
        )
        cls.istance_system = System.objects.create(
            name = "Test",
            coordinate = Point(0,0,0),
            created_by=cls.istance_user,
            updated_by=cls.istance_user,
        )
        
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
        starType, starType_create = StarType.objects.get_or_create(name="test_luminosity")
        starLuminosity, starLuminosity_create = StarLuminosity.objects.get_or_create(name="test_starType")
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
from django.test import TestCase

from ed_body.models import Planet, Star, BaseBody
from ed_system.models import System
from users.models import User

class BodyTestCase(TestCase):

    databases = '__all__'
    
    @classmethod
    def setUpTestData(cls):
        cls.istance_user = User.objects.create_user(
            username="test",
        )
        cls.istance_system = System.objects.create(
            name = "Test",
            x=0, z=0, y=0,
            created_by=cls.istance_user,
            updated_by=cls.istance_user,
        )
        
    def test_create_basebody(self):
        try:
            instance = BaseBody.objects.create(
                name="test_create_basebody",
                system=self.istance_system,
                bodyID=1,
                created_by=self.istance_user,
                updated_by=self.istance_user,
            )
        except Exception as e:
            self.fail(e)
        else:
            self.assertEqual(type(instance), BaseBody)
            self.assertEqual(instance.name, "test_create_basebody")

    def test_planet_creation(self):
        try:
            istance_Planet = Planet.objects.create(
                name = "test_planet_creation",
                system = self.istance_system,
                bodyID = 2,
                created_by=self.istance_user,
                updated_by=self.istance_user,
            )
        except Exception as e:
            self.fail(e)
        else:
            self.assertEqual(type(istance_Planet), Planet)
            self.assertEqual(istance_Planet.name, "test_planet_creation")

    def test_create_children_planet(self):
        try:
            instanceBaseBody = BaseBody.objects.create(
                name="test_create_children_planet",
                system=self.istance_system,
                bodyID=4,
                created_by=self.istance_user,
                updated_by=self.istance_user,
            )
        except Exception as e:
            self.fail(e)
        else:
            self.assertEqual(type(instanceBaseBody), BaseBody)
            self.assertEqual(instanceBaseBody.name, "test_create_children_planet")
            try:
                instancePlanet = Planet.objects.create(
                    name = "test_create_children_planet",
                    system=self.istance_system,
                    bodyID=4,
                    updated_by=self.istance_user,
                )
            except Exception as e:
                self.fail(e)
            else:
                self.assertEqual(type(instancePlanet), Planet)
                self.assertEqual(instancePlanet.name, "test_create_children_planet")
                self.assertEqual(instancePlanet.basebody_ptr, instanceBaseBody)

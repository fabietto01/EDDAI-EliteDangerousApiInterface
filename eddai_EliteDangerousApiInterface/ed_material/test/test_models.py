from django.test import TestCase
from django.core.exceptions import ValidationError

from ed_material.models import MaterialInPlanet, Material
from ed_body.models import Planet
from ed_system.models import System
from users.models import User


class MaterialTestCase(TestCase):
    """
    Test case for testing the creation and relationships of the Material model.
    
    Classes:
        MaterialTestCase: Test case for creating and validating the Material model.
    
    Methods:
        setUpTestData(cls):
            Sets up initial data for the test case, including creating a user.
        test_create_material(self):
            Tests the creation of a Material instance and validates its attributes.
        test_material_types(self):
            Tests the creation of Material instances with different types.
        test_material_grades(self):
            Tests the creation of Material instances with different grades.
    """
    
    @classmethod
    def setUpTestData(cls):
        cls.istance_user = User.objects.create_user(
            username="MaterialTestCase_user",
        )

    def test_create_material(self):
        instance = Material.objects.create(
            name="test_create_material",
            type=Material.MaterialType.RAW,
            grade=Material.MaterialGrade.COMMON,
        )
        self.assertEqual(type(instance), Material)
        self.assertEqual(instance.name, "test_create_material")
        self.assertEqual(instance.type, Material.MaterialType.RAW)
        self.assertEqual(instance.grade, Material.MaterialGrade.COMMON)

    def test_material_types(self):
        material_raw = Material.objects.create(
            name="test_material_raw",
            type=Material.MaterialType.RAW,
            grade=Material.MaterialGrade.STANDARD,
        )
        material_manufactured = Material.objects.create(
            name="test_material_manufactured",
            type=Material.MaterialType.MANUFACTURED,
            grade=Material.MaterialGrade.RARE,
        )
        material_encoded = Material.objects.create(
            name="test_material_encoded",
            type=Material.MaterialType.ENCODED,
            grade=Material.MaterialGrade.VER_RARE,
        )
        self.assertEqual(material_raw.type, Material.MaterialType.RAW)
        self.assertEqual(material_manufactured.type, Material.MaterialType.MANUFACTURED)
        self.assertEqual(material_encoded.type, Material.MaterialType.ENCODED)

    def test_material_grades(self):
        material = Material.objects.create(
            name="test_material_grade",
            type=Material.MaterialType.RAW,
            grade=Material.MaterialGrade.VER_COMMON,
        )
        self.assertEqual(material.grade, Material.MaterialGrade.VER_COMMON)
        material.grade = Material.MaterialGrade.VER_RARE
        material.save()
        material.refresh_from_db()
        self.assertEqual(material.grade, Material.MaterialGrade.VER_RARE)


class MaterialInPlanetTestCase(TestCase):
    """
    Test case for testing the creation and relationships of the MaterialInPlanet model.
    
    Classes:
        MaterialInPlanetTestCase: Test case for creating and validating the MaterialInPlanet model.
    
    Methods:
        setUpTestData(cls):
            Sets up initial data for the test case, including creating a user, system, planet, and materials.
        test_create_materialinplanet(self):
            Tests the creation of a MaterialInPlanet instance and validates its attributes.
        test_clean_model_raw_material(self):
            Tests the clean method of the MaterialInPlanet model to ensure only RAW materials can be added.
        test_unique_constraint(self):
            Tests that the same material cannot be added to the same planet twice.
        test_percent_validators(self):
            Tests the percent field validators to ensure values are between 0 and 100.
    """
    
    fixtures = ['user', 'economy', 'system', 'body', 'bgs', 'exploration', 'material']

    @classmethod
    def setUpTestData(cls):
        cls.istance_user = User.objects.create_user(
            username="MaterialInPlanetTestCase_user",
        )
        cls.istance_system = System.objects.get(name="Sol")
        cls.istance_planet = Planet.objects.create(
            name="MaterialInPlanetTestCase_planet",
            system=cls.istance_system,
            bodyID=1,
            created_by=cls.istance_user,
            updated_by=cls.istance_user,
        )
        cls.material_raw = Material.objects.create(
            name="MaterialInPlanetTestCase_raw",
            type=Material.MaterialType.RAW,
            grade=Material.MaterialGrade.COMMON,
        )
        cls.material_manufactured = Material.objects.create(
            name="MaterialInPlanetTestCase_manufactured",
            type=Material.MaterialType.MANUFACTURED,
            grade=Material.MaterialGrade.RARE,
        )

    def test_create_materialinplanet(self):
        instance = MaterialInPlanet.objects.create(
            planet=self.istance_planet,
            material=self.material_raw,
            percent=50.5,
            created_by=self.istance_user,
            updated_by=self.istance_user,
        )
        self.assertEqual(type(instance), MaterialInPlanet)
        self.assertEqual(instance.planet, self.istance_planet)
        self.assertEqual(instance.material, self.material_raw)
        self.assertEqual(instance.percent, 50.5)

    def test_clean_model_raw_material(self):
        instance = MaterialInPlanet(
            planet=self.istance_planet,
            material=self.material_manufactured,
            percent=30.0,
            created_by=self.istance_user,
            updated_by=self.istance_user,
        )
        with self.assertRaises(ValidationError):
            instance.clean()

    def test_unique_constraint(self):
        MaterialInPlanet.objects.create(
            planet=self.istance_planet,
            material=self.material_raw,
            percent=40.0,
            created_by=self.istance_user,
            updated_by=self.istance_user,
        )
        with self.assertRaises(Exception):
            MaterialInPlanet.objects.create(
                planet=self.istance_planet,
                material=self.material_raw,
                percent=50.0,
                created_by=self.istance_user,
                updated_by=self.istance_user,
            )

    def test_percent_validators(self):
        # Test valid percent values
        instance_valid = MaterialInPlanet.objects.create(
            planet=self.istance_planet,
            material=self.material_raw,
            percent=75.0,
            created_by=self.istance_user,
            updated_by=self.istance_user,
        )
        self.assertEqual(instance_valid.percent, 75.0)
        
        # Test invalid percent (negative)
        instance_invalid_negative = MaterialInPlanet(
            planet=self.istance_planet,
            material=Material.objects.create(
                name="test_material_negative",
                type=Material.MaterialType.RAW,
                grade=Material.MaterialGrade.STANDARD,
            ),
            percent=-10.0,
            created_by=self.istance_user,
            updated_by=self.istance_user,
        )
        with self.assertRaises(ValidationError):
            instance_invalid_negative.full_clean()
        
        # Test invalid percent (over 100)
        instance_invalid_over = MaterialInPlanet(
            planet=self.istance_planet,
            material=Material.objects.create(
                name="test_material_over",
                type=Material.MaterialType.RAW,
                grade=Material.MaterialGrade.STANDARD,
            ),
            percent=150.0,
            created_by=self.istance_user,
            updated_by=self.istance_user,
        )
        with self.assertRaises(ValidationError):
            instance_invalid_over.full_clean()


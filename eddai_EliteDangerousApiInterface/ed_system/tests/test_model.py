from django.test import TestCase
from django.contrib.gis.geos import Point
from django.core.exceptions import ValidationError
from django.db import IntegrityError

import random

from ed_system.models import System
from users.models import User
from ed_bgs.models import MinorFaction, MinorFactionInSystem, Faction, Government
from ed_economy.models import Economy

class SystemTestCase(TestCase):
    """
    Test suite for the System model.
    This test case includes the following tests:
    - `test_create_system`: Verifies that a system can be created with the correct attributes.
    - `test_unique_name_constraint`: Ensures that the system name is unique and raises an IntegrityError if a duplicate name is used.
    - `test_unique_coordinate_constraint`: Ensures that the system coordinates are unique and raises an IntegrityError if duplicate coordinates are used.
    - `test_system_economy_property`: Tests the economy property of the system, ensuring it correctly associates primary and secondary economies.
    - `test_system_clean_method`: Tests the clean method of the system, ensuring it raises a ValidationError when necessary and passes when conditions are met.
    - `test_system_str_method`: Verifies the string representation of the system.
    - `test_system_distance`: Tests the distance calculation between two systems.
    """
    
    @classmethod
    def setUpTestData(cls):
        cls.istance_user = User.objects.create_user(
            username="SystemTestCase",
        )

    def test_create_system(self):
        system = System.objects.create(
            name="test_create_system",
            address=random.getrandbits(16),
            coordinate=Point(0, 0, 0, srid=4979),
            created_by=self.istance_user,
            updated_by=self.istance_user,
        )
        self.assertEqual(system.name, "test_create_system")
        self.assertEqual(system.coordinate, Point(0, 0, 0, srid=4979))
        self.assertEqual(system.security, None)
        self.assertEqual(system.population, 0)
        self.assertEqual(system.description, None)

    def test_unique_name_constraint(self):
        System.objects.create(
            name="Unique Name Test System",
            address=random.getrandbits(16),
            coordinate=Point(0, 0, 0),
            created_by=self.istance_user,
            updated_by=self.istance_user,
        )
        with self.assertRaises(IntegrityError):
            System.objects.create(
                name="Unique Name Test System",
                address=random.getrandbits(16),
                coordinate=Point(1, 1, 1),
                created_by=self.istance_user,
                updated_by=self.istance_user,
            )
    
    def test_unique_coordinate_constraint(self):
        System.objects.create(
            name="Unique Coordinate Test System",
            address=random.getrandbits(16),
            coordinate=Point(2, 2, 2),
            created_by=self.istance_user,
            updated_by=self.istance_user,
        )
        with self.assertRaises(IntegrityError):
            System.objects.create(
                name="Unique Coordinate Test System 2",
                address=random.getrandbits(16),
                coordinate=Point(2, 2, 2),
                created_by=self.istance_user,
                updated_by=self.istance_user,
            )
        
    def test_system_economy_property(self):
        primary_economy = Economy.objects.create(name="Primary Economy")
        secondary_economy = Economy.objects.create(name="Secondary Economy")
        system = System.objects.create(
            name="Economy Test System",
            address=random.getrandbits(16),
            coordinate=Point(3, 3, 3),
            primaryEconomy=primary_economy,
            secondaryEconomy=secondary_economy,
            created_by=self.istance_user,
            updated_by=self.istance_user,
        )
        self.assertEqual(system.economy, [primary_economy, secondary_economy])

    def test_system_clean_method(self):
        faction = Faction.objects.create(name="test_system_clean_method")
        government = Government.objects.create(name="test_system_clean_method")
        minor_faction = MinorFaction.objects.create(
            name="test_system_clean_method",
            allegiance=faction,
            government=government,
            created_by=self.istance_user,
            updated_by=self.istance_user,
        )
        system = System.objects.create(
            name="Clean Method Test System",
            address=random.getrandbits(16),
            coordinate=Point(4, 4, 4),
            conrollingFaction=minor_faction,
            created_by=self.istance_user,
            updated_by=self.istance_user,
        )
        with self.assertRaises(ValidationError):
            system.clean()

        MinorFactionInSystem.objects.create(
            system=system, minorFaction=minor_faction,
            created_by=self.istance_user,
            updated_by=self.istance_user,
        )

        try:
            system.clean()
        except ValidationError:
            self.fail("clean() raised ValidationError unexpectedly!")

    def test_system_str_method(self):
        system = System.objects.create(
            name="Test System",
            address=random.getrandbits(16),
            coordinate=Point(5, 5, 5),
            created_by=self.istance_user,
            updated_by=self.istance_user,
        )
        self.assertEqual(str(system), "Test System")

    def test_system_distance(self):
        system1 = System.objects.create(
            name="Distance Test System 1",
            address=random.getrandbits(16),
            coordinate=Point(8, 7, 6, srid=4979),
            created_by=self.istance_user,
            updated_by=self.istance_user,
        )
        system2 = System.objects.create(
            name="Distance Test System 2",
            address=random.getrandbits(16),
            coordinate=Point(3, 4, 0, srid=4979),
            created_by=self.istance_user,
            updated_by=self.istance_user,
        )
        distance = System.get_distance(system1, system2)
        self.assertEqual(distance, 8.367)     
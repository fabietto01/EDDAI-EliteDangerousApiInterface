from django.test import TestCase
from django.contrib.gis.geos import Point

import random

from users.models import User
from ed_system.models import System
from ed_system.manager import SystemQuerySet

class SystemQuerySetTestCase(TestCase):

    fixtures = ['user', 'economy', 'system', 'body', 'bgs', 'exploration', 'material', 'mining', 'station']

    @classmethod
    def setUpTestData(cls):
        cls.istance_user = User.objects.create_user(
            username="SystemQuerySetTestCase",
        )

    def test_distance_from_system(self):
        sol = System.objects.get(name='Sol')
        system2 = System.objects.create(
            name="test_distance_from_system",
            address=random.getrandbits(16),
            coordinate=Point(3, 4, 0, srid=4979),
            created_by=self.istance_user,
            updated_by=self.istance_user,
        )
        distance = System.objects.distance_from_system(system2).get(id=sol.id).distance_st
        self.assertEqual(distance, 5.0)

    def test_view_system_control_faction(self):
        qs = System.objects.view_system_control_faction()
        self.assertEqual(qs.count(), System.objects.count())
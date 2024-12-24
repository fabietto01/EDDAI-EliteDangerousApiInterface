from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.gis.geos import Point
from rest_framework import status

from ed_system.api.venws import System
from users.models import User

class SystemViewSetTestCase(APITestCase):
    """
    Test case for the SystemViewSet API.
    This test case includes the following tests:
    - `setUpTestData`: Sets up the initial test data, including creating a test user and two systems.
    - `test_get_request`: Tests the GET request to retrieve the list of systems and checks if the response status is 200 OK and the number of systems returned is 2.
    - `test_get_request_order_by_system`: Tests the GET request to retrieve the list of systems ordered by distance from a specific system and checks if the response status is 200 OK, the number of systems returned is 2, the systems are ordered correctly by distance, and the distance is included in the response.
    """

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser")
        cls.system1 = System.objects.create(
            name="Sol",
            coordinate = Point(0, 0, 0),
            created_by=cls.user,
            updated_by=cls.user
        )
        cls.system2 = System.objects.create(
            name="Alpha Centauri",
            coordinate = Point(3.03, -0.09, 3.16),
            created_by=cls.user,
            updated_by=cls.user
        )

    def test_get_request(self):
        response = self.client.get(reverse('system-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
    
    def test_get_request_order_by_system(self):
        response = self.client.get(reverse('system-list') + '?order_by_system=' + str(self.system1.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 2)
        self.assertEqual(response.data['results'][0]['id'], self.system1.id)
        self.assertEqual(response.data['results'][1]['id'], self.system2.id)
        self.assertTrue('distance_st' in response.data['results'][0])
        self.assertTrue('distance_st' in response.data['results'][1])
        self.assertLess(response.data['results'][0]['distance_st'], response.data['results'][1]['distance_st'])
        self.assertEqual(response.data['results'][1]['distance_st'], System.get_distance(self.system1, self.system2))

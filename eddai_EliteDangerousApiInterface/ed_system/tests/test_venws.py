from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.gis.geos import Point
from rest_framework import status
import random

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

    fixtures = ['user', 'economy', 'system', 'body', 'bgs', 'exploration', 'material', 'mining', 'station']

    def test_get_request(self):
        response = self.client.get(reverse('system-list'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data['results']), 
            System.objects.all().count()
        )
    
    def test_get_request_order_by_system(self):
        sol = System.objects.get(name='Sol')
        url = reverse('system-list')
        response = self.client.get(url, {'distance_by_system': sol.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data['results']), 
            System.objects.all().count()
        )
        for system_data in response.data['results']:
            self.assertTrue('distance_st' in system_data, f'distance_st not in system {system_data["name"]}')
        distance_st = -1
        for system_data in response.data['results']:
            self.assertLess(distance_st, system_data['distance_st'], 'distance_st not ordered correctly')
            distance_st = system_data['distance_st']
        system_data = response.data['results'][0]
        system_db = System.objects.get(id=system_data['id'])
        self.assertEqual(system_data['distance_st'], System.get_distance(sol, system_db))

    def test_get_request_filters(self):
        url = reverse('system-list')
        filter_params = {
            'security': 'H',
            'population__lt': 0,
            'primaryEconomy': 2,
            'secondaryEconomy__in': [1, 2],
            'conrollingFaction': 1,
            'created_at__lt': '2022-01-01T00:00:00Z',
            'updated_at__gt': '2022-01-01T00:00:00Z'
        }
        response = self.client.get(url, filter_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        qs = System.objects.filter(**filter_params)
        self.assertEqual(len(response.data['results']), qs.count())
        filter_params = {
            'conrollingFaction__not': 1,
            'conrollingFaction_state': 1,
            'conrollingFaction_not_state': 4
        }
        response = self.client.get(url, filter_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        qs = System.objects.view_system_control_faction().exclude(
            conrollingFaction=1
        ).filter(
            conrolling_faction_view__ed_bgs_stateinminorfactions__state=1
        ).exclude(conrolling_faction_view__ed_bgs_stateinminorfactions__state=4)
        self.assertEqual(len(response.data['results']), qs.count())
        filter_params = {
            'conrollingFaction_in_state': [1, 2],
            'conrollingFaction_not_in_state': [3, 4],
            'power': 1,
            'allegiance': 1,
            'government': 1
        }
        response = self.client.get(url, filter_params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        qs = System.objects.view_system_control_faction().exclude(
            conrolling_faction_view__ed_bgs_stateinminorfactions__state__id__in=[3, 4]
        ).filter(
            conrolling_faction_view__ed_bgs_stateinminorfactions__state__id__in=[1, 2],
            ed_bgs_powerinsystems__power=1,
            conrollingFaction__allegiance=1,
            conrollingFaction__government=1
        )
        self.assertEqual(len(response.data['results']), qs.count())
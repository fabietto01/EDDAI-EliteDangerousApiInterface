from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from ed_mining.models import (
    HotspotType,
    HotSpot,
    Ring
)

from ed_mining.api.venws import (
    RingViewSet,
    HotspotTypeViewSet,
    HotSpotInRingViewSet
)

from ed_body.models import BaseBody
from ed_system.models import System
from users.models import User

class HotspotTypeViewSetTestCase(APITestCase):
    """
    Test case for the HotspotTypeViewSet.
    """

    fixtures = ['user', 'economy', 'system', 'body', 'mining', 'body_test_data', 'ring_test_data']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='HotspotTypeViewSetTestCase_user'
        )

    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_list_hotspot_types(self):
        """
        Test the list endpoint of the HotspotTypeViewSet.
        """
        url = reverse('hotspottype-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), HotspotType.objects.count())

    def test_search_hotspot_types(self):
        """
        Test the search functionality of the HotspotTypeViewSet.
        """
        hotspotType = HotspotType.objects.first()
        url = reverse('hotspottype-list')
        response = self.client.get(url, {'search': hotspotType.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)
        self.assertTrue(
            any([hotspotType.name in item['name'] for item in response.data['results']])
        )

    def test_delete_hotspot_type(self):
        """
        Test the delete endpoint of the HotspotTypeViewSet.
        """
        hotspotType = HotspotType.objects.first()
        url = reverse('hotspottype-detail', args=[hotspotType.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_create_hotspot_type(self):
        """
        Test the create endpoint of the HotspotTypeViewSet.
        """
        url = reverse('hotspottype-list')
        data = {
            'name': 'Test Hotspot Type',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

class RingViewSetTestCase(APITestCase):

    """
    Test case for the RingViewSet.
    """

    fixtures = ['user', 'economy', 'system', 'body', 'mining', 'body_test_data', 'ring_test_data']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='RingViewSetTestCase_user'
        )
    
    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_list_rings(self):
        """
        Test the list endpoint of the RingViewSet.
        """
        url = reverse('ring-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), Ring.objects.count())

    def test_search_rings(self):
        """
        Test the search functionality of the RingViewSet.
        """
        ring = Ring.objects.first()
        url = reverse('ring-list')
        response = self.client.get(url, {'search': ring.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)
        self.assertTrue(
            any([ring.pk == item['id'] for item in response.data['results']])
        )

    def test_filter_type(self):
        """
        Test the filter functionality of the RingViewSet.
        """
        ring = Ring.objects.first()
        url = reverse('ring-list')
        response = self.client.get(url, {'ringType': ring.ringType})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)
        self.assertTrue(
            all([ring.ringType == item['type'] for item in response.data['results']])
        )

    def test_filter_ring_type_in(self):
        """
        Test the filter functionality of the RingViewSet for ring type.
        """
        ringTypes = [
            Ring.RingType.Icy,
            Ring.RingType.METAL_RICH
        ]
        url = reverse('ring-list')
        response = self.client.get(url, 
            {'ringType__in': ','.join(ringTypes)}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)
        self.assertTrue(
            all([item['type'] in ringTypes for item in response.data['results']]),
            msg=f"Expected ring types {ringTypes} but got {[item['type'] for item in response.data['results']]}"
        )

    def test_filter_body(self):
        body = Ring.objects.first().body
        url = reverse('ring-list')
        response = self.client.get(url, {'body': body.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)
        self.assertTrue(
            all([body.pk == item['body']['id'] for item in response.data['results']])
        )

    def test_filter_hotspot_type(self):
        """
        Test the filter functionality of the RingViewSet.
        """
        ring = Ring.objects.get(name="Earth Ring")
        hotSpot = HotSpot.objects.filter(ring=ring).first()
        url = reverse('ring-list')
        response = self.client.get(url, {'hotspot_type': hotSpot.type.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)
        qs = HotSpot.objects.filter(type=hotSpot.type)
        for item in response.data['results']:
            self.assertTrue(
                qs.filter(ring_id=item['id']).exists(),
                msg=f"Expected HotSpot type {hotSpot.type} in results but got {item['name']}"
            )

    def test_filter_distance(self):
        start_system = System.objects.first()
        url = reverse('ring-list')
        response = self.client.get(url, 
            {'distance_by_system': start_system.pk}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)
        for item in response.data['results']:
            self.assertIn(
                'distance_st', item,
                msg=f"Expected 'distance' in result but got {item}"
            )
            self.assertEqual(
                item['distance_st'],
                System.get_distance(
                    start_system, 
                    System.objects.get(pk=item['system']['id'])
                ),
                msg=f"Expected distance to match for system {item['system']['id']}, "
                    f"but got {item['distance_st']} instead of {System.get_distance(start_system, System.objects.get(pk=item['system']['id']))}"
            )

    def test_create_ring(self):
        """
        Test the create endpoint of the RingViewSet.
        """
        url = reverse('ring-list')
        data = {
            'name': 'Test Ring',
            'body_id': BaseBody.objects.first().id,
            'type': Ring.RingType.Icy,
            "innerRad": 0,
            "outerRad": 2,
            "massMT": 0
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_ring_detail(self):
        """
        Test the detail endpoint of the RingViewSet.
        """
        ring = Ring.objects.first()
        url = reverse('ring-detail', args=[ring.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], ring.pk)

class HotSpotInRingViewSetTestCase(APITestCase):
    """
    Test case for the HotSpotInRingViewSet.
    """

    fixtures = ['user', 'economy', 'system', 'body', 'mining', 'body_test_data', 'ring_test_data']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='HotSpotInRingViewSetTestCase_user'
        )
    
    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_list_hotspots_in_ring(self):
        """
        Test the list endpoint of the HotSpotInRingViewSet.
        """
        ring = Ring.objects.first()
        url = reverse('hotspot-list', args=[ring.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], HotSpot.objects.filter(ring=ring).count())

    def test_add_hotspot_in_ring(self):
        """
        Test the create endpoint of the HotSpotInRingViewSet.
        """
        ring = Ring.objects.first()
        url = reverse('hotspot-list', args=[ring.pk])
        qs = HotspotType.objects.exclude(
            id__in = HotSpot.objects.filter(ring=ring).values_list('type', flat=True)
        )
        data = {
            'type_id': qs.first().id,
            'count': 10
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_add_multiple_hotspots_in_ring(self):
        """
        Test the multiple adds endpoint of the HotSpotInRingViewSet.
        """
        ring = Ring.objects.first()
        url = reverse('hotspot-adds', args=[ring.pk])
        qs = HotspotType.objects.exclude(
            id__in = HotSpot.objects.filter(ring=ring).values_list('type', flat=True)
        )
        data = [
            {
                'type_id': qs.first().id,
                'count': 10
            },
            {
                'type_id': qs.last().id,
                'count': 5
            }
        ]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
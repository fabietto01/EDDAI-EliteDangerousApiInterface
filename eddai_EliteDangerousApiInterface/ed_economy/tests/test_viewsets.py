from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.gis.geos import Point
import random

from ed_economy.api.serializers import (
    CompactedCommoditySerializer, CommoditySerializer,
    EconomyBasicInformationSerializer, EconomySerializer,
    CommodityInStationSerializer
)

from ed_economy.models import (
    Commodity, Economy,
    CommodityInStation
)

from users.models import User


class EconomyViewSetTestCase(APITestCase):

    fixtures = ['user', 'economy',]

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='EconomyViewSetTestCase_user')

    def setUp(self):
        super().setUp()
        self.client.logout()
    
    def test_list_economy(self):
        url = reverse('economy-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], Economy.objects.count())
        serializer = EconomyBasicInformationSerializer(
            Economy.objects.all(),
            many=True,
        )
        for result, expected in zip(response.data['results'], serializer.data):
            self.assertEqual(result, expected)
    
    def test_search_economy(self):
        economy = Economy.objects.first()
        url = reverse('economy-list')
        response = self.client.get(url, {'search': economy.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertTrue(
            any(result['id'] == economy.id for result in response.data['results']),
        )

    def test_retrieve_economy(self):
        economy = Economy.objects.first()
        url = reverse('economy-detail', args=[economy.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = EconomySerializer(economy)
        self.assertEqual(response.data, serializer.data)

    def test_delete_economy(self):
        economy = Economy.objects.first()
        url = reverse('economy-detail', args=[economy.id])
        self.client.login(username=self.user.username, password='password')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_economy(self):
        url = reverse('economy-list')
        data = {
            'name': 'Test Economy',
            'description': 'Test description',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

class CommodityViewSetTestCase(APITestCase):

    fixtures = ['user', 'economy',]

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='CommodityViewSetTestCase_User'
        )

    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_list_commodity(self):
        url = reverse('commodity-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], Commodity.objects.count())
        serializer = CompactedCommoditySerializer(
            Commodity.objects.all(),
            many=True,
        )
        for result, expected in zip(response.data['results'], serializer.data):
            self.assertEqual(result, expected)

    def test_search_commodity(self):
        commodity = Commodity.objects.first()
        url = reverse('commodity-list')
        response = self.client.get(url, {'search': commodity.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertTrue(
            any(result['id'] == commodity.id for result in response.data['results']),
        )

    def test_retrieve_commodity(self):
        commodity = Commodity.objects.first()
        url = reverse('commodity-detail', args=[commodity.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CommoditySerializer(commodity)
        self.assertEqual(response.data, serializer.data)

    def test_delete_commodity(self):
        commodity = Commodity.objects.first()
        url = reverse('commodity-detail', args=[commodity.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_commodity(self):
        url = reverse('commodity-list')
        data = {
            'name': 'Test Commodity',
            'description': 'Test description',
            'meanPrice': random.randint(1, 1000),
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

class CommodityInStationViewSetTestCase(APITestCase):

    fixtures = ['user', 'economy', 'system', 'station', 'bgs', 'economy_test_data']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='CommodityInStationViewSet_User'
        )
        cls.station = CommodityInStation.objects.first().station

    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_list_commodity_in_station(self):
        url = reverse('commodityinstation-list', kwargs={'station_pk': self.station.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        queryset = CommodityInStation.objects.filter(station=self.station)
        self.assertEqual(response.data['count'], queryset.count())
        serializer = CommodityInStationSerializer(
            queryset,
            many=True,
        )
        for result, expected in zip(response.data['results'], serializer.data):
            self.assertEqual(result, expected)

    def test_search_commodity_in_station(self):
        url = reverse('commodityinstation-list', kwargs={'station_pk': self.station.pk})
        commodity = CommodityInStation.objects.first().commodity
        response = self.client.get(url, {'search': commodity.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)
        self.assertTrue(
            any(result['commodity'] == commodity.name for result in response.data['results']),
        )

    def test_retrieve_commodity_in_station(self):
        instance = CommodityInStation.objects.first()
        url = reverse(
            'commodityinstation-detail',
            kwargs={
                'station_pk': self.station.pk,
                'pk': instance.id
            }
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = CommodityInStationSerializer(
            instance
        )
        self.assertDictEqual(
            response.data,
            serializer.data
        )
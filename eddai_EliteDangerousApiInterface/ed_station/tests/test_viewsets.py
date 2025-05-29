from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from ed_station.models import (
    Station, StationType, Service,
    ServiceInStation
)

from ed_station.api.venws import (
    StationViewSet, ServiceInStationViewSet, ServiceViewSet,
    StationTypeViewSet
)

from ed_system.models import System
from users.models import User

class StationViewSetTests(APITestCase):

    fixtures = ['user', 'economy', 'system', 'body', 'bgs', 'station', 'station_test_data']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username=cls.__class__.__name__,
        )
        cls.station = Station.objects.first()

    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_list_stations(self):
        url = reverse('station-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), Station.objects.count())

    def test_search_stations(self):
        url = reverse('station-list')
        response = self.client.get(url, {'search': 'Abraham Lincoln'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)
        self.assertTrue(
            any(station['name'] == 'Abraham Lincoln' for station in response.data['results'])
        )

    def test_filter_by_system(self):
        """Test filtering stations by system ID (exact match)"""
        url = reverse('station-list')
        response = self.client.get(url, {'system': '11'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verifica che tutte le stazioni restituite appartengano al sistema 11
        for station in response.data['results']:
            self.assertEqual(station['system']['id'], 11)

    def test_filter_by_landing_pad(self):
        """Test filtering stations by landing pad type (exact match)"""
        url = reverse('station-list')
        response = self.client.get(url, {'landingPad': 'L'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verifica che tutte le stazioni restituite abbiano landingPad 'L'
        for station in response.data['results']:
            self.assertEqual(station['landingPad'], 'L')

    def test_filter_by_primary_economy(self):
        """Test filtering stations by primary economy (in filter)"""
        url = reverse('station-list')
        # Test con economy 8 (dalla stazione Abraham Lincoln)
        response = self.client.get(url, {'primaryEconomy__in': 8})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for station in response.data['results']:
            self.assertEqual(
                station['primaryEconomy']['id'], 8,
                msg=f"Expected primary economy 8, got {station['primaryEconomy']['id']}"
            )

        # Test con multiple economies
        response = self.client.get(url, {'primaryEconomy__in': "8,1"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for station in response.data['results']:
            self.assertIn(station['primaryEconomy']['id'], [1, 8])

    def test_filter_by_secondary_economy(self):
        """Test filtering stations by secondary economy (in filter)"""
        url = reverse('station-list')
        # Test con economy 17 (presente in entrambe le stazioni)
        response = self.client.get(url, {'secondaryEconomy': 17})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for station in response.data['results']:
            self.assertEqual(station['secondaryEconomy']['id'], 17)

    def test_filter_by_minor_faction(self):
        """Test filtering stations by minor faction (in filter)"""
        url = reverse('station-list')
        # Test con minor faction 3163 (dalla stazione Abraham Lincoln)
        response = self.client.get(url, {'minorFaction': '3163'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for station in response.data['results']:
            self.assertEqual(
                station['minorFaction']['id'], 3163,
                msg=f"Expected minor faction 3163, got {station}"
            )

    def test_filter_by_service_exact(self):
        """Test filtering stations by service (exact match)"""
        url = reverse('station-list')
        # Test con service 27 (presente nella stazione Abraham Lincoln)
        response = self.client.get(url, {'service': '27'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verifica che le stazioni restituite abbiano il servizio 27
        self.assertGreater(len(response.data['results']), 0)

    def test_filter_by_service_in(self):
        """Test filtering stations by multiple services (in filter)"""
        url = reverse('station-list')
        # Test con multiple services (27, 2 presenti nella stazione Abraham Lincoln)
        response = self.client.get(url, {'service': '27', 'service': '2'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verifica che ci siano risultati
        self.assertGreater(len(response.data['results']), 0)

    def test_filter_by_distance_lt(self):
        """Test filtering stations by distance less than (lt filter)"""
        url = reverse('station-list')
        # Test con distanza < 1000 (dovrebbe includere Abraham Lincoln con 490.665508)
        response = self.client.get(url, {'distance__lt': '1000'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for station in response.data['results']:
            self.assertLess(station['distance'], 1000)

    def test_filter_by_distance_gt(self):
        """Test filtering stations by distance greater than (gt filter)"""
        url = reverse('station-list')
        # Test con distanza > 5000 (dovrebbe includere Navarrete's Prospect con 9144.208117)
        response = self.client.get(url, {'distance__gt': '5000'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for station in response.data['results']:
            self.assertGreater(station['distance'], 5000)

    def test_combined_filters(self):
        """Test using multiple filters together"""
        url = reverse('station-list')
        # Test combinando system e landingPad
        response = self.client.get(url, {
            'system': '11',
            'landingPad': 'L'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for station in response.data['results']:
            self.assertEqual(station['system']['id'], 11)
            self.assertEqual(station['landingPad'], 'L')

    def test_create_station_unauthorized(self):
        """Test that unauthorized users cannot create a station"""
        url = reverse('station-list')
        data = {
            'name': 'Test Station',
            'system_id': 11,
            'type_id': 1,
            'landingPad': 'L',
            'primaryEconomy_id': 8,
            'secondaryEconomy_id': 17,
            'minorFaction_id': 3163
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_station_authorized(self):
        """Test that authorized users can create a station"""
        self.client.force_login(self.user)
        url = reverse('station-list')
        data = {
            'name': 'Test Station',
            'markerid': 5745494,
            'system_id': 11,
            'type_id': 1,
            'landingPad': 'L',
            'primaryEconomy_id': 8,
            'secondaryEconomy_id': 17,
            'minorFaction_id': 3163
        }
        response = self.client.post(url, data)
        self.assertEqual(
            response.status_code, status.HTTP_201_CREATED,
            msg=f"Expected status code 201, got {response.status_code}, with error message {response.data}"
        )
        self.assertEqual(data.pop('system_id', None), response.data['system']['id'])
        self.assertEqual(data.pop('type_id', None), response.data['type']['id'])
        self.assertEqual(data.pop('primaryEconomy_id', None), response.data['primaryEconomy']['id'])
        self.assertEqual(data.pop('secondaryEconomy_id', None), response.data['secondaryEconomy']['id'])
        self.assertEqual(data.pop('minorFaction_id', None), response.data['minorFaction']['id'])
        for key, value in data.items():
            self.assertEqual(
                response.data[key], value, 
                msg=f"Expected {key} to be {value}, got {response.data[key]}"
            )

    def test_get_station_detail(self):
        """Test retrieving a single station by ID"""
        url = reverse('station-detail', args=[self.station.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.station.id)
        self.assertEqual(response.data['name'], self.station.name)

    def test_update_station_unauthorized(self):
        """Test that unauthorized users cannot update a station"""
        url = reverse('station-detail', args=[self.station.id])
        data = {
            'name': 'Updated Station Name'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_station_authorized(self):
        """Test that authorized users can update a station"""
        self.client.force_login(self.user)
        url = reverse('station-detail', args=[self.station.id])
        data = {
            'name': 'Updated Station Name'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Updated Station Name')

class ServiceInStationViewSetTests(APITestCase):

    fixtures = ['user', 'economy', 'system', 'body', 'bgs', 'station', 'station_test_data']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username=cls.__class__.__name__,
        )
        cls.station = Station.objects.get(id=2042)

    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_list_services_in_station(self):
        """Test listing services in a specific station"""
        url = reverse('serviceinstation-list', args=[self.station.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreater(len(response.data['results']), 0)

    def test_create_service_in_station_unauthorized(self):
        """Test that unauthorized users cannot create a service in a station"""
        url = reverse('serviceinstation-list', args=[self.station.id])
        data = {
            'service': 'carrierfuel',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_service_in_station_authorized(self):
        """Test that authorized users can create a service in a station"""
        self.client.force_login(self.user)
        url = reverse('serviceinstation-list', args=[self.station.id])
        data = {
            'service': 'carrierfuel',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['service'], 'carrierfuel')

    def test_update_service_in_station_unauthorized(self):
        """Test that unauthorized users cannot update a service in a station"""
        service_in_station = ServiceInStation.objects.filter(station=self.station).first()
        url = reverse('serviceinstation-detail', args=[self.station.id, service_in_station.id])
        data = {
            'service': 'engineer',
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_service_in_station_authorized(self):
        """Test that authorized users can update a service in a station"""
        self.client.force_login(self.user)
        service_in_station = ServiceInStation.objects.filter(station=self.station).first()
        url = reverse('serviceinstation-detail', args=[self.station.id, service_in_station.id])
        data = {
            'service': 'engineer',
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['service'], 'engineer')
    
    def test_delete_service_in_station_unauthorized(self):
        """Test that unauthorized users cannot delete a service in a station"""
        service_in_station = ServiceInStation.objects.filter(station=self.station).first()
        url = reverse('serviceinstation-detail', args=[self.station.id, service_in_station.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_service_in_station_authorized(self):
        """Test that authorized users can delete a service in a station"""
        self.client.force_login(self.user)
        service_in_station = ServiceInStation.objects.filter(station=self.station).first()
        url = reverse('serviceinstation-detail', args=[self.station.id, service_in_station.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(ServiceInStation.objects.filter(id=service_in_station.id).exists())

    def test_multiple_add_service_in_station_unauthorized(self):
        """Test that unauthorized users cannot add multiple services in a station"""
        url = reverse('serviceinstation-multiple-adds', args=[self.station.id])
        data = [
            {'service': 'carrierfuel'},
            {'service': 'livery'}
        ]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_multiple_add_service_in_station_authorized(self):
        """Test that authorized users can add multiple services in a station"""
        self.client.force_login(self.user)
        url = reverse('serviceinstation-multiple-adds', args=[self.station.id])
        data = [
            {'service': 'carrierfuel'},
            {'service': 'livery'}
        ]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 2)
        self.assertIn('carrierfuel', [item['service'] for item in response.data])
        self.assertIn('livery', [item['service'] for item in response.data])

class ServiceViewSetTests(APITestCase):

    fixtures = ['user', 'economy', 'system', 'body', 'bgs', 'station', 'station_test_data']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username=cls.__class__.__name__,
        )
        cls.station = Station.objects.get(id=2042)

    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_list_services(self):
        """Test listing all services"""
        url = reverse('service-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), Service.objects.count())
        for service in response.data['results']:
            self.assertIn('name', service)
            self.assertIn('id', service)


    def test_create_service_unauthorized(self):
        """Test that unauthorized users cannot create a service"""
        url = reverse('service-list')
        data = {
            'name': 'Test Service',
            'description': 'This is a test service.'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_service_authorized(self):
        """Test that authorized users can create a service"""
        self.client.force_login(self.user)
        url = reverse('service-list')
        data = {
            'name': 'Test Service',
            'description': 'This is a test service.'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_service_detail(self):
        """Test retrieving a single service by ID"""
        service = Service.objects.first()
        url = reverse('service-detail', args=[service.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], service.id)
        self.assertEqual(response.data['name'], service.name)
        self.assertEqual(response.data['description'], service.description)
    
    def test_update_service_unauthorized(self):
        """Test that unauthorized users cannot update a service"""
        service = Service.objects.first()
        url = reverse('service-detail', args=[service.id])
        data = {
            'name': 'Updated Service Name'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_service_authorized(self):
        """Test that authorized users can update a service"""
        self.client.force_login(self.user)
        service = Service.objects.first()
        url = reverse('service-detail', args=[service.id])
        data = {
            'name': 'Updated Service Name'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_service_unauthorized(self):
        """Test that unauthorized users cannot delete a service"""
        service = Service.objects.first()
        url = reverse('service-detail', args=[service.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_service_authorized(self):
        """Test that authorized users can delete a service"""
        self.client.force_login(self.user)
        service = Service.objects.first()
        url = reverse('service-detail', args=[service.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertTrue(Service.objects.filter(id=service.id).exists())

class StationTypeViewSetTests(APITestCase):
    fixtures = ['user', 'economy', 'system', 'body', 'bgs', 'station', 'station_test_data']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username=cls.__class__.__name__,
        )

    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_list_station_types(self):
        """Test listing all station types"""
        url = reverse('stationtype-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), StationType.objects.count())
        for station_type in response.data['results']:
            self.assertIn('name', station_type)
            self.assertIn('id', station_type)

    def test_create_station_type_unauthorized(self):
        """Test that unauthorized users cannot create a station type"""
        url = reverse('stationtype-list')
        data = {
            'name': 'Test Station Type',
            'description': 'This is a test station type.'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_station_type_authorized(self):
        """Test that authorized users can create a station type"""
        self.client.force_login(self.user)
        url = reverse('stationtype-list')
        data = {
            'name': 'Test Station Type',
            'description': 'This is a test station type.'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_get_station_type_detail(self):
        """Test retrieving a single station type by ID"""
        station_type = StationType.objects.first()
        url = reverse('stationtype-detail', args=[station_type.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], station_type.id)
        self.assertEqual(response.data['name'], station_type.name)
        self.assertEqual(response.data['description'], station_type.description)
    
    def test_update_station_type_unauthorized(self):
        """Test that unauthorized users cannot update a station type"""
        station_type = StationType.objects.first()
        url = reverse('stationtype-detail', args=[station_type.id])
        data = {
            'name': 'Updated Station Type Name'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_station_type_authorized(self):
        """Test that authorized users can update a station type"""
        self.client.force_login(self.user)
        station_type = StationType.objects.first()
        url = reverse('stationtype-detail', args=[station_type.id])
        data = {
            'name': 'Updated Station Type Name'
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
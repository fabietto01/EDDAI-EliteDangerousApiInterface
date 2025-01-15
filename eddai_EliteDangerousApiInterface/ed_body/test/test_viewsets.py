from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.gis.geos import Point
import random
from json import dumps

from ed_body.api.venws import (
    AtmosphereComponentViewSet, AtmosphereTypeViewSet,
    AtmosphereComponentInPlanetViewSet
)
from ed_body.api.serializers import (
    CompactedAtmosphereComponentSerializer, AtmosphereComponentSerializer,
    CompactedAtmosphereTypeSerializer, AtmosphereTypeSerializer,
    AtmosphereComponentInPlanetSerializer
)

from ed_body.models import (
    AtmosphereComponent, AtmosphereType,
    AtmosphereComponentInPlanet,

    Planet
)

from ed_system.models import System
from users.models import User

class AtmosphereComponentViewSetAPITestCase(APITestCase):
    """
    Test suite for the AtmosphereComponentViewSet viewset.
    Classes:
        AtmosphereComponentViewSetAPITestCase(APITestCase): Test suite for the AtmosphereComponentViewSet viewset.
    Methods:
        test_get_list_atmosphere_components(self):
            Tests the GET method for retrieving a list of atmosphere components.
        test_get_search_atmosphere_component(self):
            Tests the GET method for searching for an atmosphere component.
        test_get_retrieve_atmosphere_component(self):
            Tests the GET method for retrieving a single atmosphere component.
        test_delete_atmosphere_component(self):
            Tests the DELETE method for deleting an atmosphere component.
        test_post_atmosphere_component(self):
            Tests the POST method for creating a new atmosphere
    """
    

    fixtures = ['user', 'economy', 'system', 'body']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='AtmosphereComponentViewSetAPITestCase_User',
        )

    def setUp(self):
        super().setUp()
        self.client.logout()
    
    def test_get_list_atmosphere_components(self):
        url = reverse('atmospherecomponent-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], AtmosphereComponent.objects.count())
        serializer = CompactedAtmosphereComponentSerializer(AtmosphereComponent.objects.all(), many=True)
        for result, expected in zip(response.data['results'], serializer.data):
            self.assertDictEqual(result, expected)

    def test_get_search_atmosphere_component(self):
        atmosphere_component = AtmosphereComponent.objects.first()
        url = reverse('atmospherecomponent-list')
        response = self.client.get(url, {'search': atmosphere_component.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)
        self.assertTrue(
            any(result['id'] == atmosphere_component.id for result in response.data['results'])
        )

    def test_get_retrieve_atmosphere_component(self):
        atmosphere_component = AtmosphereComponent.objects.first()
        url = reverse('atmospherecomponent-detail', args=[atmosphere_component.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = AtmosphereComponentSerializer(atmosphere_component)
        self.assertDictEqual(response.data, serializer.data)

    def test_delete_atmosphere_component(self):
        atmosphere_component = AtmosphereComponent.objects.first()
        url = reverse('atmospherecomponent-detail', args=[atmosphere_component.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_post_atmosphere_component(self):
        url = reverse('atmospherecomponent-list')
        data = {
            'name': 'Test Atmosphere Component',
            'note': 'Test note'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

class AtmosphereTypeViewSetAPITestCase(APITestCase):
    """
    Test suite for the AtmosphereTypeViewSet viewset.
    Classes:
        AtmosphereTypeViewSetAPITestCase(APITestCase): Test suite for the AtmosphereTypeViewSet viewset.
    Methods:
        test_get_list_atmosphere_types(self):
            Tests the GET method for retrieving a list of atmosphere types.
        test_get_search_atmosphere_type(self):
            Tests the GET method for searching for an atmosphere type.
        test_get_retrieve_atmosphere_type(self):
            Tests the GET method for retrieving a single atmosphere type.
        test_delete_atmosphere_type(self):
            Tests the DELETE method for deleting an atmosphere type.
        test_post_atmosphere_type(self):
            Tests the POST method for creating a new atmosphere type.
    """
    
    fixtures = ['user', 'economy', 'system', 'body']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='AtmosphereTypeViewSetAPITestCase_User'
        )

    def setUp(self):
        super().setUp()
        self.client.logout()
    
    def test_get_list_atmosphere_types(self):
        url = reverse('atmospheretype-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], AtmosphereType.objects.count())
        serializer = CompactedAtmosphereTypeSerializer(AtmosphereType.objects.all(), many=True)
        for result, expected in zip(response.data['results'], serializer.data):
            self.assertDictEqual(result, expected)

    def test_get_search_atmosphere_type(self):
        atmosphere_type = AtmosphereType.objects.first()
        url = reverse('atmospheretype-list')
        response = self.client.get(url, {'search': atmosphere_type.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)
        self.assertTrue(
            any(result['id'] == atmosphere_type.id for result in response.data['results'])
        )

    def test_get_retrieve_atmosphere_type(self):
        atmosphere_type = AtmosphereType.objects.first()
        url = reverse('atmospheretype-detail', args=[atmosphere_type.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = AtmosphereTypeSerializer(atmosphere_type)
        self.assertDictEqual(response.data, serializer.data)

    def test_delete_atmosphere_type(self):
        atmosphere_type = AtmosphereType.objects.first()
        url = reverse('atmospheretype-detail', args=[atmosphere_type.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_atmosphere_type(self):
        url = reverse('atmospheretype-list')
        data = {
            'name': 'Test Atmosphere Type',
            'note': 'Test note'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

class AtmosphereComponentInPlanetViewSetAPITestCase(APITestCase):

    fixtures = ['user', 'economy', 'system', 'body']

    @staticmethod
    def _generate_percent():
        temp_percent = []
        remaining = 100
        while remaining > 0:
            value = random.randint(1, remaining)
            temp_percent.append(value)
            remaining -= value
        return temp_percent

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='AtmosphereComponentInPlanetViewSetAPITestCase_User',
        )
        cls.system = System.objects.create(
            name='AtmosphereComponentInPlanetViewSetAPITestCase_System',
            coordinate=Point(50, 95483, 50),
            created_by=cls.user,
            updated_by=cls.user
        )
        cls.planet = Planet.objects.create(
            name='AtmosphereComponentInPlanetViewSetAPITestCase?planet',
            system=cls.system,
            bodyID=1,
            created_by=cls.user,
            updated_by=cls.user
        )
        queryset = AtmosphereComponent.objects.all()
        for atmosphereComponent, percent in zip(queryset, cls._generate_percent()):
            AtmosphereComponentInPlanet.objects.create(
                planet=cls.planet,
                atmosphere_component=atmosphereComponent,
                percent=percent,
                created_by=cls.user,
                updated_by=cls.user
            )

    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_get_list_atmosphere_components_in_planet(self):
        url = reverse('atmospherecomponentinplanet-list', kwargs={'planet_pk': self.planet.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        queryset = AtmosphereComponentInPlanet.objects.filter(planet_id=self.planet.pk)
        self.assertEqual(response.data['count'], queryset.count())
        serializer = AtmosphereComponentInPlanetSerializer(queryset, many=True)
        for result, expected in zip(response.data['results'], serializer.data):
            self.assertDictEqual(result, expected)

    def test_search_atmosphere_component_in_planet(self):
        atmosphere_component_in_planet = AtmosphereComponentInPlanet.objects.filter(planet_id=self.planet.pk).first()
        url = reverse('atmospherecomponentinplanet-list', kwargs={'planet_pk': self.planet.pk})
        response = self.client.get(url, {'search': atmosphere_component_in_planet.atmosphere_component.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)
        self.assertTrue(
            any(result['id'] == atmosphere_component_in_planet.id for result in response.data['results'])
        )
    
    def test_retrieve_atmosphere_component_in_planet(self):
        atmosphere_component_in_planet = AtmosphereComponentInPlanet.objects.filter(planet_id=self.planet.pk).first()
        url = reverse('atmospherecomponentinplanet-detail', kwargs={'planet_pk': self.planet.pk, 'pk': atmosphere_component_in_planet.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = AtmosphereComponentInPlanetSerializer(atmosphere_component_in_planet)
        self.assertDictEqual(response.data, serializer.data)

    def test_delete_atmosphere_component_in_planet(self):
        atmosphere_component_in_planet = AtmosphereComponentInPlanet.objects.filter(planet_id=self.planet.pk).first()
        url = reverse('atmospherecomponentinplanet-detail', kwargs={'planet_pk': self.planet.pk, 'pk': atmosphere_component_in_planet.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotIn(atmosphere_component_in_planet, AtmosphereComponentInPlanet.objects.filter(planet_id=self.planet.pk))

    def test_post_atmosphere_component_in_planet(self):
        planet = Planet.objects.create(
            name='test_post_atmosphere_component_in_planet_Planet',
            system=self.system,
            bodyID=2,
            created_by=self.user,
            updated_by=self.user
        )
        url = reverse('atmospherecomponentinplanet-list', kwargs={'planet_pk': planet.pk})
        atmosphere_component = AtmosphereComponent.objects.first()
        data = {
            'atmosphere': atmosphere_component.name,
            'percent': random.randint(1, 100)
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(AtmosphereComponentInPlanet.objects.filter(id=response.data['id']).exists())
        atmosphere_componen_in_panet = AtmosphereComponentInPlanet.objects.get(id=response.data['id'])
        self.assertEqual(atmosphere_componen_in_panet.planet, planet)
        self.assertEqual(atmosphere_componen_in_panet.atmosphere_component, atmosphere_component)
        self.assertEqual(atmosphere_componen_in_panet.percent, data['percent'])

    def test_put_atmosphere_component_in_planet(self):
        atmosphere_component_in_planet = AtmosphereComponentInPlanet.objects.filter(planet_id=self.planet.pk).first()
        url = reverse('atmospherecomponentinplanet-detail', kwargs={'planet_pk': self.planet.pk, 'pk': atmosphere_component_in_planet.pk})
        data = {
            'atmosphere': atmosphere_component_in_planet.atmosphere_component.name,
            'percent': random.randint(1, atmosphere_component_in_planet.percent)
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        atmosphere_component_in_planet.refresh_from_db()
        self.assertEqual(atmosphere_component_in_planet.percent, data['percent'])

    def test_multiple_add_atmosphere_components(self):
        planet = Planet.objects.create(
            name='test_multiple_add_atmosphere_components_Planet',
            system=self.system,
            bodyID=3,
            created_by=self.user,
            updated_by=self.user
        )
        url = reverse('atmospherecomponentinplanet-multiple-add', kwargs={'planet_pk': planet.pk})
        queryset = AtmosphereComponent.objects.all()
        data = [
            {
                'atmosphere': atmosphereComponent.name,
                'percent': percent
            } for atmosphereComponent, percent in zip(queryset, self._generate_percent())
        ]
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for item in response.data:
            self.assertTrue(AtmosphereComponentInPlanet.objects.filter(id=item['id']).exists())
        queryset = AtmosphereComponentInPlanet.objects.filter(planet_id=planet.pk)
        self.assertEqual(response.data, AtmosphereComponentInPlanetSerializer(queryset, many=True).data)
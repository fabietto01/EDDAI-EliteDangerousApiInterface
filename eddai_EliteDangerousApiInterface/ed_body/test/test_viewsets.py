from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.gis.geos import Point
import random

from ed_core.functions import Distanza3D
from django.db.models import F

from ed_body.api.venws import (
    AtmosphereComponentViewSet, AtmosphereTypeViewSet,
    AtmosphereComponentInPlanetViewSet,
    PlanetTypeViewSet,
    VolcanismViewSet,
    StarLuminosityViewSet,
    StarTypeViewSet,
    BaseBodyViewSet,
    PlanetViewSet,
)
from ed_body.api.serializers import (
    CompactedAtmosphereComponentSerializer, AtmosphereComponentSerializer,
    CompactedAtmosphereTypeSerializer, AtmosphereTypeSerializer,
    AtmosphereComponentInPlanetSerializer,
    PlanetTypeSerializer, CompactedPlanetTypeSerializer,
    VolcanismSerializer, CompactedVolcanismSerializer,
    StarLuminositySerializer, CompactedStarLuminositySerializer,
    StarTypeSerializer, CompactedStarTypeSerializer,
    BaseBodySerializer, BaseBodyDistanceSerializer,
    PlanetSerializer, PlanetDistanceSerializer,
)

from ed_body.models import (
    AtmosphereComponent, AtmosphereType,
    AtmosphereComponentInPlanet,
    PlanetType,
    Volcanism,
    StarLuminosity,
    StarType,
    BaseBody,
    Planet,
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
    """
    Test suite for the AtmosphereComponentInPlanetViewSet viewset.
    Classes:
        AtmosphereComponentInPlanetViewSetAPITestCase(APITestCase): Test suite for the AtmosphereComponentInPlanetViewSet viewset.
    Methods:
        test_get_list_atmosphere_components_in_planet(self):
            Tests the GET method for retrieving a list of atmosphere components in a planet.
        test_search_atmosphere_component_in_planet(self):
            Tests the GET method for searching for an atmosphere component in a planet.
        test_retrieve_atmosphere_component_in_planet(self):
            Tests the GET method for retrieving a single atmosphere component in a planet.
        test_delete_atmosphere_component_in_planet(self):
            Tests the DELETE method for deleting an atmosphere component in a planet.
        test_post_atmosphere_component_in_planet(self):
            Tests the POST method for creating a new atmosphere component in a planet.
        test_put_atmosphere_component_in_planet(self):
            Tests the PUT method for updating an atmosphere component in a planet.
        test_multiple_add_atmosphere_components(self):
            Tests the POST method for adding multiple atmosphere components in a planet.
    """

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

class PlanetTypeViewSetAPITestCase(APITestCase):

    fixtures = ['user', 'economy', 'system', 'body']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='PlanetTypeViewSetAPITestCase_User',
        )

    def setUp(self):
        super().setUp()
        self.client.logout()
    
    def test_get_list_planet_types(self):
        url = reverse('planettype-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], PlanetType.objects.count())
        serializer = CompactedPlanetTypeSerializer(PlanetType.objects.all(), many=True)
        for result, expected in zip(response.data['results'], serializer.data):
            self.assertDictEqual(result, expected)

    def test_get_search_planet_type(self):
        planet_type = PlanetType.objects.first()
        url = reverse('planettype-list')
        response = self.client.get(url, {'search': planet_type.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)
        self.assertTrue(
            any(result['id'] == planet_type.id for result in response.data['results'])
        )
    
    def test_get_detail_planet_type(self):
        planet_type = PlanetType.objects.first()
        url = reverse('planettype-detail', args=[planet_type.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = PlanetTypeSerializer(planet_type)
        self.assertDictEqual(response.data, serializer.data)
    
    def test_delete_planet_type(self):
        planet_type = PlanetType.objects.first()
        url = reverse('planettype-detail', args=[planet_type.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_planet_type(self):
        url = reverse('planettype-list')
        data = {
            'name': 'Test Planet Type',
            'note': 'Test note'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

class VolcanismViewSetAPITestCase(APITestCase):

    fixtures = ['user', 'economy', 'system', 'body']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='VolcanismViewSetAPITestCase_User'
        )

    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_get_list_volcanisms(self):
        url = reverse('volcanism-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], Volcanism.objects.count())
        serializer = CompactedVolcanismSerializer(Volcanism.objects.all(), many=True)
        for result, expected in zip(response.data['results'], serializer.data):
            self.assertDictEqual(result, expected)

    def test_get_search_volcanism(self):
        volcanism = Volcanism.objects.first()
        url = reverse('volcanism-list')
        response = self.client.get(url, {'search': volcanism.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)
        self.assertTrue(
            any(result['id'] == volcanism.id for result in response.data['results'])
        )

    def test_get_retrieve_volcanism(self):
        volcanism = Volcanism.objects.first()
        url = reverse('volcanism-detail', args=[volcanism.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = VolcanismSerializer(volcanism)
        self.assertDictEqual(response.data, serializer.data)

    def test_delete_volcanism(self):
        volcanism = Volcanism.objects.first()
        url = reverse('volcanism-detail', args=[volcanism.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_volcanism(self):
        url = reverse('volcanism-list')
        data = {
            'name': 'Test Volcanism',
            'note': 'Test note'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

class StarLuminosityViewSetAPITestCase(APITestCase):

    fixtures = ['user', 'economy', 'system', 'body']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='StarLuminosityViewSetAPITestCase_User'
        )

    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_get_list_star_luminosities(self):
        url = reverse('starluminosity-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], StarLuminosity.objects.count())
        serializer = CompactedStarLuminositySerializer(StarLuminosity.objects.all(), many=True)
        for result, expected in zip(response.data['results'], serializer.data):
            self.assertDictEqual(result, expected)

    def test_get_search_star_luminosity(self):
        star_luminosity = StarLuminosity.objects.first()
        url = reverse('starluminosity-list')
        response = self.client.get(url, {'search': star_luminosity.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)
        self.assertTrue(
            any(result['id'] == star_luminosity.id for result in response.data['results'])
        )

    def test_get_retrieve_star_luminosity(self):
        star_luminosity = StarLuminosity.objects.first()
        url = reverse('starluminosity-detail', args=[star_luminosity.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = StarLuminositySerializer(star_luminosity)
        self.assertDictEqual(response.data, serializer.data)

    def test_delete_star_luminosity(self):
        star_luminosity = StarLuminosity.objects.first()
        url = reverse('starluminosity-detail', args=[star_luminosity.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_star_luminosity(self):
        url = reverse('starluminosity-list')
        data = {
            'name': 'Test Star Luminosity',
            'note': 'Test note'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

class StarTypeViewSetAPITestCase(APITestCase):

    fixtures = ['user', 'economy', 'system', 'body']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='StarTypeViewSetAPITestCase_User'
        )

    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_get_list_star_types(self):
        url = reverse('startype-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], StarType.objects.count())
        serializer = CompactedStarTypeSerializer(StarType.objects.all(), many=True)
        for result, expected in zip(response.data['results'], serializer.data):
            self.assertDictEqual(result, expected)

    def test_get_search_star_type(self):
        star_type = StarType.objects.first()
        url = reverse('startype-list')
        response = self.client.get(url, {'search': star_type.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)
        self.assertTrue(
            any(result['id'] == star_type.id for result in response.data['results'])
        )

    def test_get_retrieve_star_type(self):
        star_type = StarType.objects.first()
        url = reverse('startype-detail', args=[star_type.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = StarTypeSerializer(star_type)
        self.assertDictEqual(response.data, serializer.data)

    def test_delete_star_type(self):
        star_type = StarType.objects.first()
        url = reverse('startype-detail', args=[star_type.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_post_star_type(self):
        url = reverse('startype-list')
        data = {
            'name': 'Test Star Type',
            'note': 'Test note'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

class BaseBodyViewSetAPITestCase(APITestCase):

    fixtures = ['user', 'economy', 'system', 'body', 'body_test_data']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='BaseBodyViewSetAPITestCase_User'
        )

    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_get_list_base_body(self):
        url = reverse('basebody-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], BaseBody.objects.count())
        serializer = BaseBodySerializer(BaseBody.objects.all().order_by('name'), many=True)
        for result, expected in zip(response.data['results'], serializer.data):
            self.assertDictEqual(result, expected)

    def test_get_search_base_body(self):
        base_body = BaseBody.objects.first()
        url = reverse('basebody-list')
        response = self.client.get(url, {'search': base_body.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)
        self.assertTrue(
            any(result['id'] == base_body.id for result in response.data['results'])
        )
    
    def test_get_distance_base_body(self):
        system = System.objects.first()
        baseBody_count = BaseBody.objects.count()
        url = reverse('basebody-list')
        response = self.client.get(url, {'distance_by_system': system.pk})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], baseBody_count)
        self.assertTrue(
            all(result['distance_st'] for result in response.data['results'])
        )
        qs =  BaseBody.objects.annotate(
            distance_st=Distanza3D(
                F('system__coordinate'),
                point=system.coordinate
            )
        )
        serializer = BaseBodyDistanceSerializer(qs.order_by('distance_st'), many=True)
        for result, expected in zip(response.data['results'], serializer.data):
            self.assertDictEqual(result, expected)
        response = self.client.get(url, {'distance_by_system': system.pk, 'order_distance_by_system':'-distance_st'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], baseBody_count)
        serializer = BaseBodyDistanceSerializer(qs.order_by('-distance_st'), many=True)
        for result, expected in zip(response.data['results'], serializer.data):
            self.assertDictEqual(result, expected)
        
    def test_chek_distance_base_body(self):
        from_sistem = System.objects.first()        
        url = reverse('basebody-list')
        response = self.client.get(url, {'distance_by_system': from_sistem.pk, 'order_distance_by_system':'-distance_st'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        first_response:dict = response.data['results'][0]
        response_distance = first_response['distance_st']
        response_system = System.objects.get(pk=first_response['system']['id'])
        self.assertTrue(
            System.get_distance(from_sistem, response_system) == response_distance
        )

    def test_post_base_body(self):
        url = reverse('basebody-list')
        system = System.objects.first()
        data = {
            'name': 'Test Base Body',
            'system': system.pk,
            'bodyID': 1,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

class PlanetViewSetAPITestCase(APITestCase):

    fixtures = ['user', 'economy', 'system', 'body', 'body_test_data']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='PlanetViewSetAPITestCase_User'
        )

    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_get_list_planets(self):
        url = reverse('planet-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], Planet.objects.count())
        serializer = PlanetSerializer(Planet.objects.all().order_by('name'), many=True)
        for result, expected in zip(response.data['results'], serializer.data):
            self.assertDictEqual(result, expected)
    
    def test_get_search_planet(self):
        planet = Planet.objects.first()
        url = reverse('planet-list')
        response = self.client.get(url, {'search': planet.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)
        self.assertTrue(
            any(result['id'] == planet.id for result in response.data['results'])
        )
    
    def test_get_details_planet(self):
        planet = Planet.objects.first()
        url = reverse('planet-detail', args=[planet.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = PlanetSerializer(planet)
        self.assertDictEqual(response.data, serializer.data)

    def test_patch_planet(self):
        planet = Planet.objects.first()
        url = reverse('planet-detail', args=[planet.pk])
        data = {
            'name': 'Test Planet',
            'bodyID': 1
        }
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        planet.refresh_from_db()
        self.assertEqual(planet.name, data['name'])

    def test_delete_planet(self):
        planet = Planet.objects.first()
        url = reverse('planet-detail', args=[planet.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Planet.objects.filter(pk=planet.pk).exists())


from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.gis.geos import Point
import random

from ed_material.api.venws import (
    MaterialViewSet,
    MaterialInPlanetViewSet
)
from ed_material.api.serializers import (
    CompactedMaterialSerializer, MaterialSerializer,
    MaterialInPlanetSerializer
)

from ed_material.models import (
    Material,
    MaterialInPlanet
)

from ed_body.models import Planet
from ed_system.models import System
from users.models import User

class MaterialViewSetAPITestCase(APITestCase):
    """
    Test suite for the MaterialViewSet viewset.
    Classes:
        MaterialViewSetAPITestCase(APITestCase): Test suite for the MaterialViewSet viewset.
    Methods:
        test_get_list_materials(self):
            Tests the GET method for retrieving a list of materials.
        test_get_search_material(self):
            Tests the GET method for searching for a material.
        test_get_retrieve_material(self):
            Tests the GET method for retrieving a single material.
        test_delete_material(self):
            Tests the DELETE method for deleting a material.
        test_post_material(self):
            Tests the POST method for creating a new material
    """
    

    fixtures = ['user', 'economy', 'system', 'body', 'material']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='MaterialViewSetAPITestCase_User',
        )

    def setUp(self):
        super().setUp()
        self.client.logout()
    
    def test_get_list_materials(self):
        url = reverse('material-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], Material.objects.count())
        serializer = CompactedMaterialSerializer(Material.objects.all(), many=True)
        for result, expected in zip(response.data['results'], serializer.data):
            self.assertDictEqual(result, expected)

    def test_get_search_material(self):
        material = Material.objects.first()
        url = reverse('material-list')
        response = self.client.get(url, {'search': material.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)
        self.assertTrue(
            any(result['id'] == material.id for result in response.data['results'])
        )

    def test_get_retrieve_material(self):
        material = Material.objects.first()
        url = reverse('material-detail', args=[material.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = MaterialSerializer(material)
        self.assertDictEqual(response.data, serializer.data)

    def test_delete_material(self):
        material = Material.objects.first()
        url = reverse('material-detail', args=[material.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_post_material(self):
        url = reverse('material-list')
        data = {
            'name': 'Test Material',
            'type': Material.MaterialType.RAW,
            'grade': Material.MaterialGrade.COMMON,
            'note': 'Test note'
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

class MaterialInPlanetViewSetAPITestCase(APITestCase):
    """
    Test suite for the MaterialInPlanetViewSet viewset.
    Classes:
        MaterialInPlanetViewSetAPITestCase(APITestCase): Test suite for the MaterialInPlanetViewSet viewset.
    Methods:
        test_get_list_materials_in_planet(self):
            Tests the GET method for retrieving a list of materials in a planet.
        test_search_material_in_planet(self):
            Tests the GET method for searching for a material in a planet.
        test_retrieve_material_in_planet(self):
            Tests the GET method for retrieving a single material in a planet.
        test_delete_material_in_planet(self):
            Tests the DELETE method for deleting a material in a planet.
        test_post_material_in_planet(self):
            Tests the POST method for creating a new material in a planet.
        test_put_material_in_planet(self):
            Tests the PUT method for updating a material in a planet.
        test_multiple_add_materials(self):
            Tests the POST method for adding multiple materials in a planet.
    """

    fixtures = ['user', 'economy', 'system', 'body', 'material']

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
            username='MaterialInPlanetViewSetAPITestCase_User',
        )
        cls.system = System.objects.create(
            name='MaterialInPlanetViewSetAPITestCase_System',
            address=random.getrandbits(16),
            coordinate=Point(50, 95483, 50),
            created_by=cls.user,
            updated_by=cls.user
        )
        cls.planet = Planet.objects.create(
            name='MaterialInPlanetViewSetAPITestCase_planet',
            system=cls.system,
            bodyID=1,
            created_by=cls.user,
            updated_by=cls.user
        )
        # Only use RAW materials as per validation in MaterialInPlanet
        queryset = Material.objects.filter(type=Material.MaterialType.RAW)
        for material, percent in zip(queryset, cls._generate_percent()):
            MaterialInPlanet.objects.create(
                planet=cls.planet,
                material=material,
                percent=percent,
                created_by=cls.user,
                updated_by=cls.user
            )

    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_get_list_materials_in_planet(self):
        url = reverse('materialinplanet-list', kwargs={'planet_pk': self.planet.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        queryset = MaterialInPlanet.objects.filter(planet_id=self.planet.pk)
        self.assertEqual(response.data['count'], queryset.count())
        serializer = MaterialInPlanetSerializer(queryset, many=True)
        for result, expected in zip(response.data['results'], serializer.data):
            self.assertDictEqual(result, expected)

    def test_search_material_in_planet(self):
        material_in_planet = MaterialInPlanet.objects.filter(planet_id=self.planet.pk).first()
        url = reverse('materialinplanet-list', kwargs={'planet_pk': self.planet.pk})
        response = self.client.get(url, {'search': material_in_planet.material.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)
        self.assertTrue(
            any(result['id'] == material_in_planet.id for result in response.data['results'])
        )
    
    def test_retrieve_material_in_planet(self):
        material_in_planet = MaterialInPlanet.objects.filter(planet_id=self.planet.pk).first()
        url = reverse('materialinplanet-detail', kwargs={'planet_pk': self.planet.pk, 'pk': material_in_planet.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = MaterialInPlanetSerializer(material_in_planet)
        self.assertDictEqual(response.data, serializer.data)

    def test_delete_material_in_planet(self):
        material_in_planet = MaterialInPlanet.objects.filter(planet_id=self.planet.pk).first()
        url = reverse('materialinplanet-detail', kwargs={'planet_pk': self.planet.pk, 'pk': material_in_planet.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertNotIn(material_in_planet, MaterialInPlanet.objects.filter(planet_id=self.planet.pk))

    def test_post_material_in_planet(self):
        planet = Planet.objects.create(
            name='test_post_material_in_planet_Planet',
            system=self.system,
            bodyID=2,
            created_by=self.user,
            updated_by=self.user
        )
        url = reverse('materialinplanet-list', kwargs={'planet_pk': planet.pk})
        material = Material.objects.filter(type=Material.MaterialType.RAW).first()
        data = {
            'material': material.name,
            'percent': random.randint(1, 100)
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(MaterialInPlanet.objects.filter(id=response.data['id']).exists())
        material_in_planet = MaterialInPlanet.objects.get(id=response.data['id'])
        self.assertEqual(material_in_planet.planet, planet)
        self.assertEqual(material_in_planet.material, material)
        self.assertEqual(material_in_planet.percent, data['percent'])

    def test_put_material_in_planet(self):
        material_in_planet = MaterialInPlanet.objects.filter(planet_id=self.planet.pk).first()
        url = reverse('materialinplanet-detail', kwargs={'planet_pk': self.planet.pk, 'pk': material_in_planet.pk})
        data = {
            'material': material_in_planet.material.name,
            'percent': random.randint(1, int(material_in_planet.percent))
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        material_in_planet.refresh_from_db()
        self.assertEqual(material_in_planet.percent, data['percent'])

    def test_multiple_add_materials(self):
        planet = Planet.objects.create(
            name='test_multiple_add_materials_Planet',
            system=self.system,
            bodyID=3,
            created_by=self.user,
            updated_by=self.user
        )
        url = reverse('materialinplanet-multiple-adds', kwargs={'planet_pk': planet.pk})
        queryset = Material.objects.filter(type=Material.MaterialType.RAW)
        data = [
            {
                'material': material.name,
                'percent': percent
            } for material, percent in zip(queryset, self._generate_percent())
        ]
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data=data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for item in response.data:
            self.assertTrue(MaterialInPlanet.objects.filter(id=item['id']).exists())
        queryset = MaterialInPlanet.objects.filter(planet_id=planet.pk)
        self.assertEqual(response.data, MaterialInPlanetSerializer(queryset, many=True).data)

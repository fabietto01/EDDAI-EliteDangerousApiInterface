from rest_framework.test import APITestCase
from django.urls import reverse
from ed_system.models import System
from users.models import User
from ed_system.api.venws import SystemViewSet
from ed_system.api.serializers.SystemSerializer import SystemSerializer, SystemDistanceSerializer

class SystemViewSetTestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username="testuser")
        cls.system1 = System.objects.create(
            name="Alpha",
            x=0, y=0, z=0,
            created_by=cls.user,
            updated_by=cls.user
        )
        cls.system2 = System.objects.create(
            name="Beta",
            x=1, y=1, z=1,
            created_by=cls.user,
            updated_by=cls.user
        )

    def test_default_serializer_class(self):
        viewset = SystemViewSet()
        viewset.request = self.client.get(reverse('system-list')).wsgi_request
        serializer_class = viewset.get_serializer_class()
        self.assertEqual(serializer_class, SystemSerializer)

    def test_distance_serializer_class(self):
        viewset = SystemViewSet()
        viewset.request = self.client.get(reverse('system-list'), {'order_by_system': 'true'}).wsgi_request
        serializer_class = viewset.get_serializer_class()
        self.assertEqual(serializer_class, SystemDistanceSerializer)

    def test_queryset(self):
        viewset = SystemViewSet()
        queryset = viewset.get_queryset()
        self.assertEqual(list(queryset), [self.system1, self.system2])

    def test_search_functionality(self):
        response = self.client.get(reverse('system-list'), {'search': 'Alpha'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Alpha')
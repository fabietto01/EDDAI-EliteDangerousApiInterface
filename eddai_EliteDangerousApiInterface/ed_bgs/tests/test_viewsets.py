from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

from ed_bgs.api.serializers import (
    FactionBasicInformationSerializer, FactionSerializer,
    GovernmentBasicInformationSerializer, GovernmentSerializer,
    StateBasicInformationSerializer, StateSerializer,
    PowerStateBasicInformationSerializer, PowerStateSerializer,
    PowerBasicInformationSerializer, PowerSerializer,
    MinorFactionBasicInformation, MinorFactionSerializer,
    MinorFactionInSystemBasicInformationSerializer,
    MinorFactionInSystemSerializer,
    MinorFactionInSystemFromMinorFactionSerializer,
    MinorFactionInSystemFromsystemSerializer,
    StateInMinorFactionSerializer,
    PowerInSystemBasicInformationSerializer,
    PowerInSystemSerializer,
    PowerInSystemFromSystemSerializer,
)

from ed_bgs.models import (
    Faction, Government, State, PowerState, Power,
    MinorFaction, MinorFactionInSystem,
    StateInMinorFaction, PowerInSystem
)

from users.models import User


class FactionViewSetTestCase(APITestCase):

    fixtures = ['user', 'economy', 'system', 'bgs']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='FactionViewSetTestCase_user')

    def setUp(self):
        super().setUp()
    
    def test_list_faction(self):
        url = reverse('faction-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], Faction.objects.count())
        serializer = FactionBasicInformationSerializer(
            Faction.objects.all(),
            many=True,
        )
        for result, expected in zip(response.data['results'], serializer.data):
            self.assertEqual(result, expected)
    
    def test_search_faction(self):
        faction = Faction.objects.first()
        url = reverse('faction-list')
        response = self.client.get(url, {'search': faction.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertTrue(
            any(result['id'] == faction.id for result in response.data['results']),
        )

    def test_retrieve_faction(self):
        faction = Faction.objects.first()
        url = reverse('faction-detail', args=[faction.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = FactionSerializer(faction)
        self.assertEqual(response.data, serializer.data)

    def test_delete_faction(self):
        faction = Faction.objects.first()
        url = reverse('faction-detail', args=[faction.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_faction(self):
        url = reverse('faction-list')
        data = {
            'name': 'Test Faction',
            'description': 'Test description',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class GovernmentViewSetTestCase(APITestCase):

    fixtures = ['user', 'economy', 'system', 'bgs']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='GovernmentViewSetTestCase_user')

    def setUp(self):
        super().setUp()
    
    def test_list_government(self):
        url = reverse('government-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], Government.objects.count())
        serializer = GovernmentBasicInformationSerializer(
            Government.objects.all(),
            many=True,
        )
        for result, expected in zip(response.data['results'], serializer.data):
            self.assertEqual(result, expected)
    
    def test_search_government(self):
        government = Government.objects.first()
        url = reverse('government-list')
        response = self.client.get(url, {'search': government.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertTrue(
            any(result['id'] == government.id for result in response.data['results']),
        )

    def test_retrieve_government(self):
        government = Government.objects.first()
        url = reverse('government-detail', args=[government.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = GovernmentSerializer(government)
        self.assertEqual(response.data, serializer.data)

    def test_delete_government(self):
        government = Government.objects.first()
        url = reverse('government-detail', args=[government.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_government(self):
        url = reverse('government-list')
        data = {
            'name': 'Test Government',
            'type': 'D',
            'description': 'Test description',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class StateViewSetTestCase(APITestCase):

    fixtures = ['user', 'economy', 'system', 'bgs']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='StateViewSetTestCase_user')

    def setUp(self):
        super().setUp()
    
    def test_list_state(self):
        url = reverse('state-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], State.objects.count())
        serializer = StateBasicInformationSerializer(
            State.objects.all(),
            many=True,
        )
        for result, expected in zip(response.data['results'], serializer.data):
            self.assertEqual(result, expected)
    
    def test_search_state(self):
        state = State.objects.first()
        url = reverse('state-list')
        response = self.client.get(url, {'search': state.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertTrue(
            any(result['id'] == state.id for result in response.data['results']),
        )

    def test_retrieve_state(self):
        state = State.objects.first()
        url = reverse('state-detail', args=[state.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = StateSerializer(state)
        self.assertEqual(response.data, serializer.data)

    def test_delete_state(self):
        state = State.objects.first()
        url = reverse('state-detail', args=[state.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_state(self):
        url = reverse('state-list')
        data = {
            'name': 'Test State',
            'description': 'Test description',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class PowerStateViewSetTestCase(APITestCase):

    fixtures = ['user', 'economy', 'system', 'bgs']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='PowerStateViewSetTestCase_user')

    def setUp(self):
        super().setUp()
    
    def test_list_powerstate(self):
        url = reverse('powerstate-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], PowerState.objects.count())
        serializer = PowerStateBasicInformationSerializer(
            PowerState.objects.all(),
            many=True,
        )
        for result, expected in zip(response.data['results'], serializer.data):
            self.assertEqual(result, expected)
    
    def test_search_powerstate(self):
        powerstate = PowerState.objects.first()
        url = reverse('powerstate-list')
        response = self.client.get(url, {'search': powerstate.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertTrue(
            any(result['id'] == powerstate.id for result in response.data['results']),
        )

    def test_retrieve_powerstate(self):
        powerstate = PowerState.objects.first()
        url = reverse('powerstate-detail', args=[powerstate.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = PowerStateSerializer(powerstate)
        self.assertEqual(response.data, serializer.data)

    def test_delete_powerstate(self):
        powerstate = PowerState.objects.first()
        url = reverse('powerstate-detail', args=[powerstate.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_powerstate(self):
        url = reverse('powerstate-list')
        data = {
            'name': 'Test PowerState',
            'description': 'Test description',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class PowerViewSetTestCase(APITestCase):

    fixtures = ['user', 'economy', 'system', 'bgs']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='PowerViewSetTestCase_user')

    def setUp(self):
        super().setUp()
    
    def test_list_power(self):
        url = reverse('power-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], Power.objects.count())
        serializer = PowerBasicInformationSerializer(
            Power.objects.all(),
            many=True,
        )
        for result, expected in zip(response.data['results'], serializer.data):
            self.assertEqual(result, expected)
    
    def test_search_power(self):
        power = Power.objects.first()
        url = reverse('power-list')
        response = self.client.get(url, {'search': power.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertTrue(
            any(result['id'] == power.id for result in response.data['results']),
        )

    def test_retrieve_power(self):
        power = Power.objects.first()
        url = reverse('power-detail', args=[power.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = PowerSerializer(power)
        self.assertEqual(response.data, serializer.data)

    def test_delete_power(self):
        power = Power.objects.first()
        url = reverse('power-detail', args=[power.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_post_power(self):
        url = reverse('power-list')
        data = {
            'name': 'Test Power',
            'note': 'Test note',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class MinorFactionViewSetTestCase(APITestCase):

    fixtures = ['user', 'economy', 'system', 'bgs']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(username='MinorFactionViewSetTestCase_user')

    def setUp(self):
        super().setUp()
    
    def test_list_minorfaction(self):
        url = reverse('minorfaction-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], MinorFaction.objects.count())
        serializer = MinorFactionBasicInformation(
            MinorFaction.objects.all(),
            many=True,
        )
        for result, expected in zip(response.data['results'], serializer.data):
            self.assertEqual(result, expected)
    
    def test_search_minorfaction(self):
        minorfaction = MinorFaction.objects.first()
        url = reverse('minorfaction-list')
        response = self.client.get(url, {'search': minorfaction.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)
        self.assertTrue(
            any(result['id'] == minorfaction.id for result in response.data['results']),
        )

    def test_retrieve_minorfaction(self):
        minorfaction = MinorFaction.objects.first()
        url = reverse('minorfaction-detail', args=[minorfaction.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = MinorFactionSerializer(minorfaction)
        self.assertEqual(response.data, serializer.data)

    def test_create_minorfaction(self):
        url = reverse('minorfaction-list')
        allegiance = Faction.objects.first()
        government = Government.objects.first()
        data = {
            'name': 'Test Minor Faction',
            'allegiance': allegiance.name,
            'government': government.name,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertEqual(response.data['allegiance'], data['allegiance'])
        self.assertEqual(response.data['government'], data['government'])

    def test_update_minorfaction(self):
        minorfaction = MinorFaction.objects.first()
        url = reverse('minorfaction-detail', args=[minorfaction.id])
        data = {
            'name': 'Updated Minor Faction Name',
            'allegiance': minorfaction.allegiance.name,
            'government': minorfaction.government.name,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], data['name'])

    def test_delete_minorfaction(self):
        minorfaction = MinorFaction.objects.first()
        url = reverse('minorfaction-detail', args=[minorfaction.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(MinorFaction.objects.filter(id=minorfaction.id).exists())

    def test_get_systems_action(self):
        """Test the custom get_systems action."""
        minorfaction = MinorFaction.objects.first()
        url = reverse('minorfaction-systems', args=[minorfaction.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verify response contains systems where this minor faction is present
        systems_count = MinorFactionInSystem.objects.filter(minorFaction=minorfaction).count()
        self.assertEqual(response.data['count'], systems_count)


class MinorFactionInSystemViewSetTestCase(APITestCase):
    """Test case for MinorFactionInSystemViewSet - a standard (non-nested) viewset."""

    fixtures = ['user', 'economy', 'system', 'bgs', 'bgs_test_data']

    @classmethod
    def setUpTestData(cls):
        from ed_system.models import System
        cls.user = User.objects.create_user(username='MinorFactionInSystemViewSetTestCase_user')
        cls.system = System.objects.first()
        cls.system2 = System.objects.last()
        cls.minor_faction = MinorFaction.objects.first()
        cls.minor_faction2 = MinorFaction.objects.last()

    def setUp(self):
        super().setUp()
        # Create test data for each test
        self.mfis = MinorFactionInSystem.objects.create(
            system=self.system,
            minorFaction=self.minor_faction,
            Influence=0.5,
            created_by=self.user,
            updated_by=self.user,
        )

    def test_list_minorfactioninsystem(self):
        """Test listing all minor factions in systems."""
        url = reverse('minorfactioninsystem-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], MinorFactionInSystem.objects.count())
        serializer = MinorFactionInSystemBasicInformationSerializer(
            MinorFactionInSystem.objects.all(),
            many=True,
        )
        for result, expected in zip(response.data['results'], serializer.data):
            self.assertEqual(result, expected)

    def test_filter_by_system(self):
        """Test filtering minor factions by system."""
        # Create another MFIS in a different system
        MinorFactionInSystem.objects.create(
            system=self.system2,
            minorFaction=self.minor_faction2,
            Influence=0.3,
            created_by=self.user,
            updated_by=self.user,
        )
        url = reverse('minorfactioninsystem-list')
        response = self.client.get(url, {'system': self.system.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        queryset = MinorFactionInSystem.objects.filter(system=self.system)
        self.assertEqual(response.data['count'], queryset.count())
        # Verify all results belong to the filtered system
        for result in response.data['results']:
            self.assertEqual(result['system'], self.system.name)

    def test_filter_by_minorfaction(self):
        """Test filtering by minor faction."""
        # Create another MFIS with different faction
        MinorFactionInSystem.objects.create(
            system=self.system2,
            minorFaction=self.minor_faction2,
            Influence=0.3,
            created_by=self.user,
            updated_by=self.user,
        )
        url = reverse('minorfactioninsystem-list')
        response = self.client.get(url, {'minorFaction': self.minor_faction.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        queryset = MinorFactionInSystem.objects.filter(minorFaction=self.minor_faction)
        self.assertEqual(response.data['count'], queryset.count())
        # Verify all results belong to the filtered faction
        for result in response.data['results']:
            self.assertEqual(result['minorFaction'], self.minor_faction.name)

    def test_retrieve_minorfactioninsystem(self):
        """Test retrieving a specific minor faction in system."""
        url = reverse('minorfactioninsystem-detail', args=[self.mfis.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = MinorFactionInSystemSerializer(self.mfis)
        self.assertEqual(response.data, serializer.data)
        # Verify states field is included in detail view
        self.assertIn('states', response.data)

    def test_create_minorfactioninsystem(self):
        """Test creating a new minor faction in system record."""
        url = reverse('minorfactioninsystem-list')
        data = {
            'system': self.system.name,
            'minorFaction': self.minor_faction2.name,
            'Influence': 0.3,
        }
        # Test without authentication
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Test with authentication
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['system'], data['system'])
        self.assertEqual(response.data['minorFaction'], data['minorFaction'])
        self.assertEqual(float(response.data['Influence']), data['Influence'])
        
        # Verify the record was created
        self.assertTrue(
            MinorFactionInSystem.objects.filter(
                system=self.system,
                minorFaction=self.minor_faction2
            ).exists()
        )

    def test_update_minorfactioninsystem(self):
        """Test updating an existing minor faction in system record."""
        url = reverse('minorfactioninsystem-detail', args=[self.mfis.id])
        data = {
            'system': self.mfis.system.name,
            'minorFaction': self.mfis.minorFaction.name,
            'Influence': 0.75,
        }
        # Test without authentication
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Test with authentication
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['Influence']), data['Influence'])
        
        # Verify the record was updated
        self.mfis.refresh_from_db()
        self.assertEqual(float(self.mfis.Influence), data['Influence'])

    def test_partial_update_minorfactioninsystem(self):
        """Test partially updating a minor faction in system record."""
        url = reverse('minorfactioninsystem-detail', args=[self.mfis.id])
        data = {
            'Influence': 0.65,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(float(response.data['Influence']), data['Influence'])
        
        # Verify the record was updated
        self.mfis.refresh_from_db()
        self.assertEqual(float(self.mfis.Influence), data['Influence'])

    def test_delete_minorfactioninsystem(self):
        """Test deleting a minor faction in system record."""
        url = reverse('minorfactioninsystem-detail', args=[self.mfis.id])
        
        # Test without authentication
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Test with authentication
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify the record was deleted
        self.assertFalse(MinorFactionInSystem.objects.filter(id=self.mfis.id).exists())


class StateInMinorFactionViewSetTestCase(APITestCase):

    fixtures = ['user', 'economy', 'system', 'bgs', 'bgs_test_data']

    @classmethod
    def setUpTestData(cls):
        from ed_system.models import System
        cls.user = User.objects.create_user(username='StateInMinorFactionViewSetTestCase_user')
        system = System.objects.first()
        minor_faction = MinorFaction.objects.first()
        cls.mfis = MinorFactionInSystem.objects.create(
            system=system,
            minorFaction=minor_faction,
            Influence=0.5,
            created_by=cls.user,
            updated_by=cls.user,
        )
        cls.state = State.objects.first()
        cls.state2 = State.objects.last()
        cls.simf = StateInMinorFaction.objects.create(
            minorFaction=cls.mfis,
            state=cls.state,
            phase=StateInMinorFaction.PhaseChoices.ACTIVE,
            created_by=cls.user,
            updated_by=cls.user,
        )

    def setUp(self):
        super().setUp()

    def test_list_stateinminorfaction(self):
        url = reverse('stateinminorfaction-list', kwargs={'minorfactioninsystem_pk': self.mfis.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        queryset = StateInMinorFaction.objects.filter(minorFaction=self.mfis)
        self.assertEqual(response.data['count'], queryset.count())

    def test_retrieve_stateinminorfaction(self):
        url = reverse(
            'stateinminorfaction-detail',
            kwargs={'minorfactioninsystem_pk': self.mfis.pk, 'pk': self.simf.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = StateInMinorFactionSerializer(self.simf)
        self.assertDictEqual(response.data, serializer.data)

    def test_create_stateinminorfaction(self):
        url = reverse('stateinminorfaction-list', kwargs={'minorfactioninsystem_pk': self.mfis.pk})
        data = {
            'state': self.state2.name,
            'phase': 'A',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['state'], data['state'])

    def test_update_stateinminorfaction(self):
        url = reverse(
            'stateinminorfaction-detail',
            kwargs={'minorfactioninsystem_pk': self.mfis.pk, 'pk': self.simf.id}
        )
        data = {
            'state': self.simf.state.name,
            'phase': 'P',
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('phase', response.data)

    def test_delete_stateinminorfaction(self):
        url = reverse(
            'stateinminorfaction-detail',
            kwargs={'minorfactioninsystem_pk': self.mfis.pk, 'pk': self.simf.id}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(StateInMinorFaction.objects.filter(id=self.simf.id).exists())


class PowerInSystemViewSetTestCase(APITestCase):

    fixtures = ['user', 'economy', 'system', 'bgs', 'bgs_test_data']

    @classmethod
    def setUpTestData(cls):
        from ed_system.models import System
        cls.user = User.objects.create_user(username='PowerInSystemViewSetTestCase_user')
        cls.system = System.objects.first()
        cls.system2 = System.objects.last()
        cls.power = Power.objects.first()
        cls.power2 = Power.objects.last()
        cls.powerstate = PowerState.objects.first()
        cls.powerstate2 = PowerState.objects.last()

    def setUp(self):
        super().setUp()
        # Create test data for each test
        self.pis = PowerInSystem.objects.create(
            system=self.system,
            power=self.power,
            state=self.powerstate,
            created_by=self.user,
            updated_by=self.user,
        )

    def test_list_powerinsystem(self):
        """Test listing all powers in systems without filters."""
        url = reverse('powerinsystem-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], PowerInSystem.objects.count())
        serializer = PowerInSystemBasicInformationSerializer(
            PowerInSystem.objects.all(),
            many=True,
        )
        for result, expected in zip(response.data['results'], serializer.data):
            self.assertEqual(result, expected)

    def test_filter_by_system(self):
        """Test filtering powers in system by system."""
        # Create another PowerInSystem in a different system
        PowerInSystem.objects.create(
            system=self.system2,
            power=self.power2,
            state=self.powerstate,
            created_by=self.user,
            updated_by=self.user,
        )
        url = reverse('powerinsystem-list')
        response = self.client.get(url, {'system': self.system.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        queryset = PowerInSystem.objects.filter(system=self.system)
        self.assertEqual(response.data['count'], queryset.count())
        # Verify all results belong to the filtered system
        for result in response.data['results']:
            self.assertEqual(result['system'], self.system.name)

    def test_filter_by_power(self):
        """Test filtering by power."""
        # Create another PowerInSystem with different power
        PowerInSystem.objects.create(
            system=self.system2,
            power=self.power2,
            state=self.powerstate,
            created_by=self.user,
            updated_by=self.user,
        )
        url = reverse('powerinsystem-list')
        response = self.client.get(url, {'power': self.power.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        queryset = PowerInSystem.objects.filter(power=self.power)
        self.assertEqual(response.data['count'], queryset.count())
        # Verify all results belong to the filtered power
        for result in response.data['results']:
            self.assertEqual(result['power'], self.power.name)

    def test_filter_by_state(self):
        """Test filtering by power state."""
        # Create another PowerInSystem with different state
        PowerInSystem.objects.create(
            system=self.system2,
            power=self.power,
            state=self.powerstate2,
            created_by=self.user,
            updated_by=self.user,
        )
        url = reverse('powerinsystem-list')
        response = self.client.get(url, {'state': self.powerstate.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        queryset = PowerInSystem.objects.filter(state=self.powerstate)
        self.assertEqual(response.data['count'], queryset.count())
        # Verify all results belong to the filtered state
        for result in response.data['results']:
            self.assertEqual(result['state'], self.powerstate.name)

    def test_retrieve_powerinsystem(self):
        """Test retrieving a specific power in system."""
        url = reverse('powerinsystem-detail', args=[self.pis.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = PowerInSystemSerializer(self.pis)
        self.assertEqual(response.data, serializer.data)

    def test_create_powerinsystem(self):
        """Test creating a new power in system record."""
        url = reverse('powerinsystem-list')
        data = {
            'system': self.system2.name,
            'power': self.power2.name,
            'state': self.powerstate.name,
        }
        # Test without authentication
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Test with authentication
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['system'], data['system'])
        self.assertEqual(response.data['power'], data['power'])
        self.assertEqual(response.data['state'], data['state'])
        
        # Verify the record was created with correct owner
        created_pis = PowerInSystem.objects.get(id=response.data['id'])
        self.assertEqual(created_pis.created_by, self.user)
        self.assertEqual(created_pis.updated_by, self.user)

    def test_update_powerinsystem(self):
        """Test updating an existing power in system record."""
        url = reverse('powerinsystem-detail', args=[self.pis.id])
        data = {
            'system': self.pis.system.name,
            'power': self.pis.power.name,
            'state': self.powerstate2.name,
        }
        # Test without authentication
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Test with authentication
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['state'], data['state'])
        
        # Verify the record was updated
        self.pis.refresh_from_db()
        self.assertEqual(self.pis.state.name, data['state'])
        self.assertEqual(self.pis.updated_by, self.user)

    def test_partial_update_powerinsystem(self):
        """Test partially updating a power in system record."""
        url = reverse('powerinsystem-detail', args=[self.pis.id])
        data = {
            'state': self.powerstate2.name,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['state'], data['state'])
        
        # Verify the record was updated
        self.pis.refresh_from_db()
        self.assertEqual(self.pis.state.name, data['state'])
        self.assertEqual(self.pis.updated_by, self.user)

    def test_delete_powerinsystem(self):
        """Test deleting a power in system record."""
        url = reverse('powerinsystem-detail', args=[self.pis.id])
        
        # Test without authentication
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Test with authentication
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify the record was deleted
        self.assertFalse(PowerInSystem.objects.filter(id=self.pis.id).exists())


class MinorFactionInSystemFromSystemViewSetTestCase(APITestCase):
    """Test the nested endpoint for listing minor factions in a specific system."""

    fixtures = ['user', 'economy', 'system', 'bgs', 'bgs_test_data']

    @classmethod
    def setUpTestData(cls):
        from ed_system.models import System
        cls.user = User.objects.create_user(username='MinorFactionInSystemFromSystemViewSetTestCase_user')
        cls.system = System.objects.first()
        cls.minor_faction = MinorFaction.objects.first()
        # Create some test data
        MinorFactionInSystem.objects.create(
            system=cls.system,
            minorFaction=cls.minor_faction,
            Influence=0.5,
            created_by=cls.user,
            updated_by=cls.user,
        )

    def setUp(self):
        super().setUp()

    def test_list_minor_factions_from_system(self):
        """Test listing all minor factions in a specific system."""
        url = reverse('minor-factions-in-system-from-system-list', kwargs={'id': self.system.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        queryset = MinorFactionInSystem.objects.filter(system=self.system)
        self.assertEqual(response.data['count'], queryset.count())
        # Verify that system field is not in the response (as per MinorFactionInSystemFromsystemSerializer)
        if response.data['results']:
            self.assertNotIn('system', response.data['results'][0])
            self.assertIn('minorFaction', response.data['results'][0])


class PowerInSystemFromSystemViewSetTestCase(APITestCase):
    """Test the nested endpoint for listing powers in a specific system."""

    fixtures = ['user', 'economy', 'system', 'bgs']

    @classmethod
    def setUpTestData(cls):
        from ed_system.models import System
        cls.user = User.objects.create_user(username='PowerInSystemFromSystemViewSetTestCase_user')
        cls.system = System.objects.first()
        cls.power = Power.objects.first()
        cls.powerstate = PowerState.objects.first()
        # Create some test data
        PowerInSystem.objects.create(
            system=cls.system,
            power=cls.power,
            state=cls.powerstate,
            created_by=cls.user,
            updated_by=cls.user,
        )

    def setUp(self):
        super().setUp()

    def test_list_powers_from_system(self):
        """Test listing all powers in a specific system."""
        url = reverse('powers-in-system-list', kwargs={'id': self.system.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        queryset = PowerInSystem.objects.filter(system=self.system)
        self.assertEqual(response.data['count'], queryset.count())
        # Verify that system field is not in the response (as per PowerInSystemFromSystemSerializer)
        if response.data['results']:
            self.assertNotIn('system', response.data['results'][0])
            self.assertIn('power', response.data['results'][0])

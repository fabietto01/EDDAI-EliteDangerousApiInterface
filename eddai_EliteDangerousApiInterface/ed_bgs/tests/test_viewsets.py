from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
import random

from ed_bgs.api.serializers import (
    FactionBasicInformationSerializer, FactionSerializer,
    GovernmentBasicInformationSerializer, GovernmentSerializer,
    StateBasicInformationSerializer, StateSerializer,
    PowerStateBasicInformationSerializer, PowerStateSerializer,
    PowerBasicInformationSerializer, PowerSerializer,
    MinorFactionBasicInformation, MinorFactionSerializer,
    MinorFactionInSystemSerializer,
    StateInMinorFactionSerializer,
    PowerInSystemSerializer,
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
        self.client.logout()
    
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
        self.client.logout()
    
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
        self.client.logout()
    
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
        self.client.logout()
    
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
        self.client.logout()
    
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
        self.client.logout()
    
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
            'allegiance': allegiance.id,
            'government': government.id,
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
            'allegiance': minorfaction.allegiance.id,
            'government': minorfaction.government.id,
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


class MinorFactionInSystemViewSetTestCase(APITestCase):

    fixtures = ['user', 'economy', 'system', 'bgs', 'bgs_test_data']

    @classmethod
    def setUpTestData(cls):
        from ed_system.models import System
        cls.user = User.objects.create_user(username='MinorFactionInSystemViewSetTestCase_user')
        cls.system = System.objects.first()
        cls.minor_faction = MinorFaction.objects.first()
        cls.minor_faction2 = MinorFaction.objects.last()
        cls.mfis = MinorFactionInSystem.objects.create(
            system=cls.system,
            minorFaction=cls.minor_faction,
            Influence=0.5,
            created_by=cls.user,
            updated_by=cls.user,
        )

    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_list_minorfactioninsystem(self):
        url = reverse('minorfactioninsystem-list', kwargs={'system_pk': self.system.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        queryset = MinorFactionInSystem.objects.filter(system=self.system)
        self.assertEqual(response.data['count'], queryset.count())

    def test_retrieve_minorfactioninsystem(self):
        url = reverse(
            'minorfactioninsystem-detail',
            kwargs={'system_pk': self.system.pk, 'pk': self.mfis.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = MinorFactionInSystemSerializer(self.mfis)
        self.assertDictEqual(response.data, serializer.data)

    def test_create_minorfactioninsystem(self):
        url = reverse('minorfactioninsystem-list', kwargs={'system_pk': self.system.pk})
        data = {
            'minorFaction': self.minor_faction2.id,
            'Influence': 0.3,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['minorFaction'], data['minorFaction'])

    def test_update_minorfactioninsystem(self):
        url = reverse(
            'minorfactioninsystem-detail',
            kwargs={'system_pk': self.system.pk, 'pk': self.mfis.id}
        )
        data = {
            'minorFaction': self.mfis.minorFaction.id,
            'Influence': 0.75,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Influence'], data['Influence'])

    def test_delete_minorfactioninsystem(self):
        url = reverse(
            'minorfactioninsystem-detail',
            kwargs={'system_pk': self.system.pk, 'pk': self.mfis.id}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
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
        self.client.logout()

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
            'state': self.state2.id,
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
            'state': self.simf.state.id,
            'phase': 'P',
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['phase'], data['phase'])

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
        cls.power = Power.objects.first()
        cls.powerstate = PowerState.objects.first()
        cls.pis = PowerInSystem.objects.create(
            system=cls.system,
            power=cls.power,
            state=cls.powerstate,
            created_by=cls.user,
            updated_by=cls.user,
        )

    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_list_powerinsystem(self):
        url = reverse('powerinsystem-list', kwargs={'system_pk': self.system.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        queryset = PowerInSystem.objects.filter(system=self.system)
        self.assertEqual(response.data['count'], queryset.count())

    def test_retrieve_powerinsystem(self):
        url = reverse(
            'powerinsystem-detail',
            kwargs={'system_pk': self.system.pk, 'pk': self.pis.id}
        )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        serializer = PowerInSystemSerializer(self.pis)
        self.assertDictEqual(response.data, serializer.data)

    def test_create_powerinsystem(self):
        url = reverse('powerinsystem-list', kwargs={'system_pk': self.system.pk})
        power2 = Power.objects.last()
        data = {
            'power': power2.id,
            'state': self.powerstate.id,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['power'], data['power'])

    def test_update_powerinsystem(self):
        url = reverse(
            'powerinsystem-detail',
            kwargs={'system_pk': self.system.pk, 'pk': self.pis.id}
        )
        powerstate2 = PowerState.objects.last()
        data = {
            'power': self.pis.power.id,
            'state': powerstate2.id,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['state'], data['state'])

    def test_delete_powerinsystem(self):
        url = reverse(
            'powerinsystem-detail',
            kwargs={'system_pk': self.system.pk, 'pk': self.pis.id}
        )
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(PowerInSystem.objects.filter(id=self.pis.id).exists())

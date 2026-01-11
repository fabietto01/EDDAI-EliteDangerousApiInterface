from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from ed_exploration.models import (
    SampleSignals,
    SignalSignals,
    Sample,
    Signal
)

from ed_exploration.api.venws import (
    SampleSignalsViewSet,
    SignalSignalsViewSet,
    SampleInPlanetViewSet,
    SignalInPlanetViewSet
)

from ed_body.models import Planet
from ed_system.models import System
from users.models import User


class SampleSignalsViewSetTestCase(APITestCase):
    """
    Test case for the SampleSignalsViewSet.
    """

    fixtures = ['user', 'economy', 'system', 'body', 'exploration']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='SampleSignalsViewSetTestCase_user'
        )

    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_list_sample_signals(self):
        """
        Test the list endpoint of the SampleSignalsViewSet.
        """
        url = reverse('samplesignals-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), SampleSignals.objects.count())

    def test_search_sample_signals(self):
        """
        Test the search functionality of the SampleSignalsViewSet.
        """
        sampleSignal = SampleSignals.objects.first()
        url = reverse('samplesignals-list')
        response = self.client.get(url, {'search': sampleSignal.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)
        self.assertTrue(
            any([sampleSignal.name in item['name'] for item in response.data['results']])
        )

    def test_retrieve_sample_signal(self):
        """
        Test the retrieve endpoint of the SampleSignalsViewSet.
        """
        sampleSignal = SampleSignals.objects.first()
        url = reverse('samplesignals-detail', args=[sampleSignal.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], sampleSignal.pk)
        self.assertEqual(response.data['name'], sampleSignal.name)

    def test_delete_sample_signal(self):
        """
        Test the delete endpoint of the SampleSignalsViewSet.
        """
        sampleSignal = SampleSignals.objects.first()
        url = reverse('samplesignals-detail', args=[sampleSignal.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_create_sample_signal(self):
        """
        Test the create endpoint of the SampleSignalsViewSet.
        """
        url = reverse('samplesignals-list')
        data = {
            'name': 'Test Sample Signal',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class SignalSignalsViewSetTestCase(APITestCase):
    """
    Test case for the SignalSignalsViewSet.
    """

    fixtures = ['user', 'economy', 'system', 'body', 'exploration']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='SignalSignalsViewSetTestCase_user'
        )

    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_list_signal_signals(self):
        """
        Test the list endpoint of the SignalSignalsViewSet.
        """
        url = reverse('signalsignals-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), SignalSignals.objects.count())

    def test_search_signal_signals(self):
        """
        Test the search functionality of the SignalSignalsViewSet.
        """
        signalSignal = SignalSignals.objects.first()
        url = reverse('signalsignals-list')
        response = self.client.get(url, {'search': signalSignal.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data['results']), 1)
        self.assertTrue(
            any([signalSignal.name in item['name'] for item in response.data['results']])
        )

    def test_retrieve_signal_signal(self):
        """
        Test the retrieve endpoint of the SignalSignalsViewSet.
        """
        signalSignal = SignalSignals.objects.first()
        url = reverse('signalsignals-detail', args=[signalSignal.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], signalSignal.pk)
        self.assertEqual(response.data['name'], signalSignal.name)

    def test_delete_signal_signal(self):
        """
        Test the delete endpoint of the SignalSignalsViewSet.
        """
        signalSignal = SignalSignals.objects.first()
        url = reverse('signalsignals-detail', args=[signalSignal.pk])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_create_signal_signal(self):
        """
        Test the create endpoint of the SignalSignalsViewSet.
        """
        url = reverse('signalsignals-list')
        data = {
            'name': 'Test Signal Signal',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)


class SampleInPlanetViewSetTestCase(APITestCase):
    """
    Test case for the SampleInPlanetViewSet.
    """

    fixtures = ['user', 'economy', 'system', 'body', 'body_test_data', 'exploration', 'exploration_test_data']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='SampleInPlanetViewSetTestCase_user'
        )
    
    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_list_samples_in_planet(self):
        """
        Test the list endpoint of the SampleInPlanetViewSet.
        """
        planet = Planet.objects.first()
        self.assertTrue(planet, "No Planet available for testing.")
        url = reverse('sample-list', kwargs={'planet_pk': planet.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['count'], 
            Sample.objects.filter(planet=planet).count()
        )

    def test_search_samples_in_planet(self):
        """
        Test the search functionality of the SampleInPlanetViewSet.
        """
        planet = Planet.objects.first()
        self.assertTrue(planet, "No Planet available for testing.")
        self.assertTrue(
            Sample.objects.filter(planet=planet).exists(),
            "No Sample available for testing."
        )
        sample = Sample.objects.filter(planet=planet).first()
        url = reverse('sample-list', kwargs={'planet_pk': planet.pk})
        response = self.client.get(url, {'search': sample.type.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)

    def test_add_sample_in_planet(self):
        """
        Test the create endpoint of the SampleInPlanetViewSet.
        """
        planet = Planet.objects.first()
        self.assertTrue(planet, "No Planet available for testing.")
        existing_types = Sample.objects.filter(planet=planet).values_list('type', flat=True)
        available_type = SampleSignals.objects.exclude(id__in=existing_types).first()
        self.assertTrue(available_type, "No available SampleSignals for testing.")
        url = reverse('sample-list', kwargs={'planet_pk': planet.pk})
        data = {
            'type': available_type.name,
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['type'], available_type.name)

    def test_add_multiple_samples_in_planet(self):
        """
        Test the multiple adds endpoint of the SampleInPlanetViewSet.
        """
        planet = Planet.objects.first()
        self.assertTrue(planet, "No Planet available for testing.")
        # Find sample types not yet added to this planet
        existing_types = Sample.objects.filter(planet=planet).values_list('type', flat=True)
        available_types = SampleSignals.objects.exclude(id__in=existing_types)[:2]
        self.assertGreaterEqual(available_types.count(), 2, "Not enough available SampleSignals for testing.")
        
        url = reverse('sample-multiple-adds', kwargs={'planet_pk': planet.pk})
        data = [
            {'type': available_types[0].name},
            {'type': available_types[1].name}
        ]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 2)

    def test_add_duplicate_sample_in_planet(self):
        """
        Test adding a duplicate sample to a planet.
        """
        planet = Planet.objects.first()
        self.assertTrue(planet, "No Planet available for testing.")
        self.assertTrue(
            Sample.objects.filter(planet=planet).exists(),
            "No Sample available for testing."
        )
        existing_sample = Sample.objects.filter(planet=planet).first()
        url = reverse('sample-list', kwargs={'planet_pk': planet.pk})
        data = {
            'type': existing_sample.type.name,
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_sample_in_planet(self):
        """
        Test the retrieve endpoint of the SampleInPlanetViewSet.
        """
        planet = Planet.objects.first()
        self.assertTrue(planet, "No Planet available for testing.")
        self.assertTrue(
            Sample.objects.filter(planet=planet).exists(),
            "No Sample available for testing."
        )
        sample = Sample.objects.filter(planet=planet).first()
        url = reverse('sample-detail', kwargs={'planet_pk': planet.pk, 'pk': sample.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], sample.pk)

    def test_update_sample_in_planet(self):
        """
        Test the update endpoint of the SampleInPlanetViewSet.
        """
        planet = Planet.objects.first()
        self.assertTrue(planet, "No Planet available for testing.")
        self.assertTrue(
            Sample.objects.filter(planet=planet).exists(),
            "No Sample available for testing."
        )
        sample = Sample.objects.filter(planet=planet).first()
        new_type = SampleSignals.objects.exclude(
            id__in=Sample.objects.filter(planet=planet).values_list('type_id', flat=True)
        ).first()
        self.assertTrue(new_type, "No different SampleSignals for testing.")
        url = reverse('sample-detail', kwargs={'planet_pk': planet.pk, 'pk': sample.pk})
        data = {
            'type': new_type.name,
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['type'], new_type.name)

    def test_delete_sample_in_planet(self):
        """
        Test the delete endpoint of the SampleInPlanetViewSet.
        """
        planet = Planet.objects.first()
        self.assertTrue(planet, "No Planet available for testing.")
        self.assertTrue(
            Sample.objects.filter(planet=planet).exists(),
            "No Sample available for testing."
        )
        sample = Sample.objects.filter(planet=planet).first()
        url = reverse('sample-detail', kwargs={'planet_pk': planet.pk, 'pk': sample.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Sample.objects.filter(pk=sample.pk).exists())

    def test_add_sample_to_nonexistent_planet(self):
        """
        Test adding a sample to a non-existent planet.
        """
        url = reverse('sample-multiple-adds', kwargs={'planet_pk': 99999})
        data = [{'type': SampleSignals.objects.first().name}]
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SignalInPlanetViewSetTestCase(APITestCase):
    """
    Test case for the SignalInPlanetViewSet.
    """

    fixtures = ['user', 'economy', 'system', 'body', 'body_test_data', 'exploration', 'exploration_test_data']

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username='SignalInPlanetViewSetTestCase_user'
        )
    
    def setUp(self):
        super().setUp()
        self.client.logout()

    def test_list_signals_in_planet(self):
        """
        Test the list endpoint of the SignalInPlanetViewSet.
        """
        planet = Planet.objects.first()
        self.assertTrue(planet, "No Planet available for testing.")
        url = reverse('signal-list', kwargs={'planet_pk': planet.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data['count'], 
            Signal.objects.filter(planet=planet).count()
        )

    def test_search_signals_in_planet(self):
        """
        Test the search functionality of the SignalInPlanetViewSet.
        """
        planet = Planet.objects.first()
        self.assertTrue(planet, "No Planet available for testing.")
        self.assertTrue(
            Signal.objects.filter(planet=planet).exists(),
            "No Signal available for testing."
        )
        signal = Signal.objects.filter(planet=planet).first()
        url = reverse('signal-list', kwargs={'planet_pk': planet.pk})
        response = self.client.get(url, {'search': signal.type.name})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(response.data['count'], 1)

    def test_add_signal_in_planet(self):
        """
        Test the create endpoint of the SignalInPlanetViewSet.
        """
        planet = Planet.objects.first()
        self.assertTrue(planet, "No Planet available for testing.")
        # Find a signal type not yet added to this planet
        existing_types = Signal.objects.filter(planet=planet).values_list('type', flat=True)
        available_type = SignalSignals.objects.exclude(id__in=existing_types).first()
        self.assertTrue(available_type, "No available SignalSignals for testing.")
        
        url = reverse('signal-list', kwargs={'planet_pk': planet.pk})
        data = {
            'type': available_type.name,
            'count': 10
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['type'], available_type.name)
        self.assertEqual(response.data['count'], 10)

    def test_add_multiple_signals_in_planet(self):
        """
        Test the multiple adds endpoint of the SignalInPlanetViewSet.
        """
        planet = Planet.objects.first()
        self.assertTrue(planet, "No Planet available for testing.")
        # Find signal types not yet added to this planet
        existing_types = Signal.objects.filter(planet=planet).values_list('type', flat=True)
        available_types = SignalSignals.objects.exclude(id__in=existing_types)[:2]
        self.assertGreaterEqual(available_types.count(), 2, "Not enough available SignalSignals for testing.")
        
        url = reverse('signal-multiple-adds', kwargs={'planet_pk': planet.pk})
        data = [
            {'type': available_types[0].name, 'count': 10},
            {'type': available_types[1].name, 'count': 5}
        ]
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(response.data), 2)

    def test_add_duplicate_signal_in_planet(self):
        """
        Test adding a duplicate signal to a planet.
        """
        planet = Planet.objects.first()
        self.assertTrue(planet, "No Planet available for testing.")
        self.assertTrue(
            Signal.objects.filter(planet=planet).exists(),
            "No Signal available for testing."
        )
        existing_signal = Signal.objects.filter(planet=planet).first()
        url = reverse('signal-list', kwargs={'planet_pk': planet.pk})
        data = {
            'type': existing_signal.type.name,
            'count': 15
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_signal_in_planet(self):
        """
        Test the retrieve endpoint of the SignalInPlanetViewSet.
        """
        planet = Planet.objects.first()
        self.assertTrue(planet, "No Planet available for testing.")
        self.assertTrue(
            Signal.objects.filter(planet=planet).exists(),
            "No Signal available for testing."
        )
        signal = Signal.objects.filter(planet=planet).first()
        url = reverse('signal-detail', kwargs={'planet_pk': planet.pk, 'pk': signal.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], signal.pk)

    def test_update_signal_in_planet(self):
        """
        Test the update endpoint of the SignalInPlanetViewSet.
        """
        planet = Planet.objects.first()
        self.assertTrue(planet, "No Planet available for testing.")
        self.assertTrue(
            Signal.objects.filter(planet=planet).exists(),
            "No Signal available for testing."
        )
        signal = Signal.objects.filter(planet=planet).first()
        # Update count
        url = reverse('signal-detail', kwargs={'planet_pk': planet.pk, 'pk': signal.pk})
        data = {
            'type': signal.type.name,
            'count': 20
        }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 20)

    def test_delete_signal_in_planet(self):
        """
        Test the delete endpoint of the SignalInPlanetViewSet.
        """
        planet = Planet.objects.first()
        self.assertTrue(planet, "No Planet available for testing.")
        self.assertTrue(
            Signal.objects.filter(planet=planet).exists(),
            "No Signal available for testing."
        )
        signal = Signal.objects.filter(planet=planet).first()
        url = reverse('signal-detail', kwargs={'planet_pk': planet.pk, 'pk': signal.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Signal.objects.filter(pk=signal.pk).exists())

    def test_add_signal_with_negative_count(self):
        """
        Test adding a signal with negative count.
        """
        planet = Planet.objects.first()
        self.assertTrue(planet, "No Planet available for testing.")
        available_type = SignalSignals.objects.first()
        self.assertTrue(available_type, "No SignalSignals available for testing.")
        url = reverse('signal-list', kwargs={'planet_pk': planet.pk})
        data = {
            'type': available_type.name,
            'count': -5
        }
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_signal_to_nonexistent_planet(self):
        """
        Test adding a signal to a non-existent planet.
        """
        url = reverse('signal-multiple-adds', kwargs={'planet_pk': 99999})
        data = [{'type': SignalSignals.objects.first().name, 'count': 5}]
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

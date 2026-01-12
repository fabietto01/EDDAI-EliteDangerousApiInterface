from rest_framework.test import APITestCase

from ed_exploration.models import (
    SampleSignals,
    SignalSignals,
    Sample,
    Signal
)

from ed_exploration.api.serializers import (
    SampleSignalsSerializer,
    SignalSignalsSerializer,
    SampleSerializer,
    SignalSerializer
)

from ed_body.models import Planet
from users.models import User


BASE_SAMPLE_SIGNALS_SERIALIZER_DATA = {
    "id": 1,
    "name": "Brancae"
}

BASE_SAMPLE_SIGNALS_DESERIALIZER_DATA = {
    "name": "Test Sample Signal"
}

BASE_SIGNAL_SIGNALS_SERIALIZER_DATA = {
    "id": 2,
    "name": "Biological"
}

BASE_SIGNAL_SIGNALS_DESERIALIZER_DATA = {
    "name": "Test Signal Signal"
}


class SampleSignalsSerializerTestCase(APITestCase):
    """
    Test case for the SampleSignalsSerializer.
    """

    fixtures = ['user', 'economy', 'system', 'body', 'exploration']

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the test case.
        This method is called once for the entire test case.
        """
        cls.user = User.objects.create_user(
            username=cls.__class__.__name__,
        )

    def test_serializer(self):
        """
        Test serialization of SampleSignals model.
        """
        instance = SampleSignals.objects.get(id=1)
        serializer = SampleSignalsSerializer(instance)
        data = serializer.data
        self.assertDictEqual(
            data, BASE_SAMPLE_SIGNALS_SERIALIZER_DATA,
            msg="The serialized data does not match the expected data."
        )

    def test_deserializer(self):
        """
        Test deserialization of SampleSignals model.
        """
        serializer = SampleSignalsSerializer(data=BASE_SAMPLE_SIGNALS_DESERIALIZER_DATA)
        is_valid = serializer.is_valid()
        self.assertTrue(
            is_valid,
            msg="The deserialized data is not valid. Errors: {}".format(serializer.errors)
        )
        instance = serializer.save()
        for key, value in BASE_SAMPLE_SIGNALS_DESERIALIZER_DATA.items():
            self.assertEqual(
                getattr(instance, key), value,
                msg=f"The deserialized data does not match the expected data for field '{key}'."
            )

    def test_many_serializer(self):
        """
        Test serialization of multiple SampleSignals instances.
        """
        qs = SampleSignals.objects.all()[:5]
        serializer = SampleSignalsSerializer(qs, many=True)
        data = serializer.data
        self.assertEqual(
            len(data), qs.count(),
            msg="The serialized data does not match the expected count."
        )
        for item in data:
            self.assertIn('id', item)
            self.assertIn('name', item)


class SignalSignalsSerializerTestCase(APITestCase):
    """
    Test case for the SignalSignalsSerializer.
    """

    fixtures = ['user', 'economy', 'system', 'body', 'exploration']

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the test case.
        This method is called once for the entire test case.
        """
        cls.user = User.objects.create_user(
            username=cls.__class__.__name__,
        )

    def test_serializer(self):
        """
        Test serialization of SignalSignals model.
        """
        instance = SignalSignals.objects.get(id=2)
        serializer = SignalSignalsSerializer(instance)
        data = serializer.data
        self.assertDictEqual(
            data, BASE_SIGNAL_SIGNALS_SERIALIZER_DATA,
            msg="The serialized data does not match the expected data."
        )

    def test_deserializer(self):
        """
        Test deserialization of SignalSignals model.
        """
        serializer = SignalSignalsSerializer(data=BASE_SIGNAL_SIGNALS_DESERIALIZER_DATA)
        is_valid = serializer.is_valid()
        self.assertTrue(
            is_valid,
            msg="The deserialized data is not valid. Errors: {}".format(serializer.errors)
        )
        instance = serializer.save()
        for key, value in BASE_SIGNAL_SIGNALS_DESERIALIZER_DATA.items():
            self.assertEqual(
                getattr(instance, key), value,
                msg=f"The deserialized data does not match the expected data for field '{key}'."
            )

    def test_many_serializer(self):
        """
        Test serialization of multiple SignalSignals instances.
        """
        qs = SignalSignals.objects.all()[:5]
        serializer = SignalSignalsSerializer(qs, many=True)
        data = serializer.data
        self.assertEqual(
            len(data), qs.count(),
            msg="The serialized data does not match the expected count."
        )
        for item in data:
            self.assertIn('id', item)
            self.assertIn('name', item)


class SampleSerializerTestCase(APITestCase):
    """
    Test case for the SampleSerializer.
    """

    fixtures = ['user', 'economy', 'system', 'body', 'body_test_data', 'exploration', 'exploration_test_data']

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the test case.
        This method is called once for the entire test case.
        """
        cls.user = User.objects.create_user(
            username=cls.__class__.__name__,
        )
        # Retrieve test data from fixtures
        cls.planet = Planet.objects.first()
        cls.sample_type = SampleSignals.objects.first()
        cls.sample = Sample.objects.first()

    def test_serializer(self):
        """
        Test serialization of Sample model.
        """
        self.assertIsNotNone(self.sample, "Sample instance was not loaded from fixtures")
        serializer = SampleSerializer(self.sample)
        data = serializer.data
        self.assertIn('id', data)
        self.assertIn('type', data)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)
        self.assertNotIn('planet', data)
        self.assertEqual(data['type'], self.sample.type.name)

    def test_deserializer(self):
        """
        Test deserialization of Sample model.
        """
        self.assertTrue(Planet.objects.exists(), "No Planet objects available in database")
        self.assertTrue(SampleSignals.objects.exists(), "No SampleSignals objects available in database")
        
        planet = Planet.objects.first()
        # Get a sample type that doesn't exist for this planet yet
        existing_types = Sample.objects.filter(planet=planet).values_list('type', flat=True)
        available_type = SampleSignals.objects.exclude(id__in=existing_types).first()
        
        self.assertIsNotNone(available_type, "No available SampleSignals type for testing")
        
        data = {
            'type': available_type.name,
        }
        serializer = SampleSerializer(
            data=data,
            context={'planet_pk': planet.pk}
            )
        is_valid = serializer.is_valid()
        self.assertTrue(
            is_valid,
            msg="The deserialized data is not valid. Errors: {}".format(serializer.errors)
        )
        instance = serializer.save(
            planet=planet,
            created_by=self.user,
            updated_by=self.user
        )
        self.assertEqual(instance.type, available_type)
        self.assertEqual(instance.planet, planet)

    def test_deserializer_with_invalid_type(self):
        """
        Test deserialization with invalid sample type.
        """
        data = {
            'type': 'NonExistentSampleType',
        }
        serializer = SampleSerializer(data=data)
        is_valid = serializer.is_valid()
        self.assertFalse(
            is_valid,
            msg="The deserialized data should not be valid for non-existent type."
        )
        self.assertIn('type', serializer.errors)

    def test_many_serializer(self):
        """
        Test serialization of multiple Sample instances.
        """
        self.assertTrue(Planet.objects.exists(), "No Planet objects available in database")
        
        planet = Planet.objects.first()
        qs = Sample.objects.filter(planet=planet)[:3]
        self.assertGreater(qs.count(), 0, "No Sample objects available for the planet")
        
        serializer = SampleSerializer(qs, many=True)
        data = serializer.data
        self.assertEqual(
            len(data), qs.count(),
            msg="The serialized data does not match the expected count."
        )
        for item in data:
            self.assertIn('id', item)
            self.assertIn('type', item)

    def test_read_only_fields(self):
        """
        Test that read-only fields cannot be set during deserialization.
        """
        sample_type = SampleSignals.objects.exclude(
            id__in=Sample.objects.filter(planet=self.planet).values_list('type', flat=True)
        ).first()
        data = {
            'type': sample_type.name,
            'created_at': '2020-01-01T00:00:00Z',
            'updated_at': '2020-01-01T00:00:00Z',
        }
        serializer = SampleSerializer(
            data=data,
            context={'planet_pk': self.planet.pk}
        )
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid, msg=f"Errors: {serializer.errors}")
        instance = serializer.save(
            planet=self.planet,
            created_by=self.user,
            updated_by=self.user
        )
        self.assertNotEqual(
            instance.created_at.isoformat(), '2020-01-01T00:00:00+00:00',
            "created_at field was incorrectly set during deserialization"
        )
        self.assertNotEqual(
            instance.updated_at.isoformat(), '2020-01-01T00:00:00+00:00',
            "updated_at field was incorrectly set during deserialization"
        )
        # The created_at and updated_at should be ignored during deserialization


class SignalSerializerTestCase(APITestCase):
    """
    Test case for the SignalSerializer.
    """

    fixtures = ['user', 'economy', 'system', 'body', 'body_test_data', 'exploration', 'exploration_test_data']

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the test case.
        This method is called once for the entire test case.
        """
        cls.user = User.objects.create_user(
            username=cls.__class__.__name__,
        )
        # Retrieve test data from fixtures
        cls.planet = Planet.objects.first()
        cls.signal_type = SignalSignals.objects.get(pk=2)  # Biological
        cls.signal = Signal.objects.get(pk=1)  # Signal with type=2 (Biological) and count=5

    def test_serializer(self):
        """
        Test serialization of Signal model.
        """
        self.assertIsNotNone(self.signal, "Signal instance was not loaded from fixtures")
        serializer = SignalSerializer(self.signal)
        data = serializer.data
        self.assertIn('id', data)
        self.assertIn('type', data)
        self.assertIn('count', data)
        self.assertIn('created_at', data)
        self.assertIn('updated_at', data)
        self.assertNotIn('planet', data)
        self.assertEqual(data['type'], self.signal_type.name)
        self.assertEqual(data['count'], 5)

    def test_deserializer(self):
        """
        Test deserialization of Signal model.
        """
        self.assertTrue(Planet.objects.exists(), "No Planet objects available in database")
        self.assertTrue(SignalSignals.objects.exists(), "No SignalSignals objects available in database")
        
        planet = Planet.objects.first()
        # Get a signal type that doesn't exist for this planet yet
        existing_types = Signal.objects.filter(planet=planet).values_list('type', flat=True)
        available_type = SignalSignals.objects.exclude(id__in=existing_types).first()
        
        self.assertIsNotNone(available_type, "No available SignalSignals type for testing")
        
        data = {
            'type': available_type.name,
            'count': 10
        }
        serializer = SignalSerializer(
            data=data,
            context={'planet_pk': planet.pk}
        )
        is_valid = serializer.is_valid()
        self.assertTrue(
            is_valid,
            msg="The deserialized data is not valid. Errors: {}".format(serializer.errors)
        )
        instance = serializer.save(
            planet=planet,
            created_by=self.user,
            updated_by=self.user
        )
        self.assertEqual(instance.type, available_type)
        self.assertEqual(instance.planet, planet)
        self.assertEqual(instance.count, 10)

    def test_deserializer_with_invalid_type(self):
        """
        Test deserialization with invalid signal type.
        """
        data = {
            'type': 'NonExistentSignalType',
            'count': 5
        }
        serializer = SignalSerializer(data=data)
        is_valid = serializer.is_valid()
        self.assertFalse(
            is_valid,
            msg="The deserialized data should not be valid for non-existent type."
        )
        self.assertIn('type', serializer.errors)

    def test_deserializer_with_negative_count(self):
        """
        Test deserialization with negative count.
        """
        self.assertTrue(SignalSignals.objects.exists(), "No SignalSignals objects available in database")
        
        signal_type = SignalSignals.objects.first()
        data = {
            'type': signal_type.name,
            'count': -5
        }
        serializer = SignalSerializer(data=data)
        is_valid = serializer.is_valid()
        self.assertFalse(
            is_valid,
            msg="The deserialized data should not be valid for negative count."
        )
        self.assertIn('count', serializer.errors)

    def test_deserializer_without_count(self):
        """
        Test deserialization without count field.
        """
        self.assertTrue(SignalSignals.objects.exists(), "No SignalSignals objects available in database")
        
        signal_type = SignalSignals.objects.first()
        data = {
            'type': signal_type.name,
        }
        serializer = SignalSerializer(data=data)
        is_valid = serializer.is_valid()
        self.assertFalse(
            is_valid,
            msg="The deserialized data should not be valid without count."
        )
        self.assertIn('count', serializer.errors)

    def test_many_serializer(self):
        """
        Test serialization of multiple Signal instances.
        """
        self.assertTrue(Planet.objects.exists(), "No Planet objects available in database")
        
        planet = Planet.objects.first()
        qs = Signal.objects.filter(planet=planet)[:3]
        self.assertGreater(qs.count(), 0, "No Signal objects available for the planet")
        
        serializer = SignalSerializer(qs, many=True)
        data = serializer.data
        self.assertEqual(
            len(data), qs.count(),
            msg="The serialized data does not match the expected count."
        )
        for item in data:
            self.assertIn('id', item)
            self.assertIn('type', item)
            self.assertIn('count', item)

    def test_read_only_fields(self):
        """
        Test that read-only fields cannot be set during deserialization.
        """
        signal_type = SignalSignals.objects.exclude(
            id__in=Signal.objects.filter(planet=self.planet).values_list('type', flat=True)
        ).first()
        data = {
            'type': signal_type.name,
            'count': 5,
            'created_at': '2020-01-01T00:00:00Z',
            'updated_at': '2020-01-01T00:00:00Z',
        }
        serializer = SignalSerializer(
            data=data, context={'planet_pk': self.planet.pk}
        )
        is_valid = serializer.is_valid()
        self.assertTrue(is_valid, msg=f"Errors: {serializer.errors}")
        # The created_at and updated_at should be ignored during deserialization
        instance = serializer.save(
            planet=self.planet,
            created_by=self.user,
            updated_by=self.user
        )
        self.assertNotEqual(
            instance.created_at.isoformat(), data.get('created_at'),
            "created_at field was incorrectly set during deserialization"
        )
        self.assertNotEqual(
            instance.updated_at.isoformat(), data.get('updated_at'),
            "updated_at field was incorrectly set during deserialization"
        )

    def test_update_count(self):
        """
        Test updating the count field of a signal.
        """
        self.assertIsNotNone(self.signal, "Signal instance was not loaded from fixtures")
        
        data = {
            'type': self.signal.type.name,
            'count': 15
        }
        serializer = SignalSerializer(
            instance=self.signal,
            data=data,
            context={'planet_pk': self.planet.pk}
        )
        is_valid = serializer.is_valid()
        self.assertTrue(
            is_valid,
            msg="The deserialized data is not valid. Errors: {}".format(serializer.errors)
        )
        updated_instance = serializer.save(updated_by=self.user)
        self.assertEqual(updated_instance.count, 15)
        self.assertEqual(updated_instance.type, self.signal_type)

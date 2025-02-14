from django.test import TestCase

from eddn.service.worker.serializers import FSDJumpSerializer, DockedSerializer, LocationSerializer
from eddn.service.worker.serializers.journal.baseJournalSerializer import BaseJournalSerializer
from eddn.service.worker.dataAnalysis.journalAnalysis import JournalAnalysis
from eddn.service.worker.serializers.journal.carrierJumpSerializer import CarrierJumpSerializer

from users.models import User
from eddn.models import DataLog
import time

class BaseJournalSerializerTestCase(TestCase):

    fixtures = ['user', 'economy', 'system', 'body', 'bgs', 'exploration', 'material', 'mining', 'station','eddn_test_service_event_FSDJump']

    @classmethod
    def setUpTestData(cls):
        cls.agent = User.objects.create_user(
            username='BaseJournalSerializerTestCase'
        )

    def test_validate(self):
        for item in DataLog.objects.all():
            serializer = BaseJournalSerializer(data=item.message)
            valid = serializer.is_valid()
            self.assertTrue(valid, serializer.errors)

    def test_update(self):
        object = DataLog.objects.get(id=1)
        serializer = BaseJournalSerializer(data=object.message)
        valid = serializer.is_valid()
        self.assertTrue(valid, serializer.errors)
        instance = serializer.save(
            created_by=self.agent,
            updated_by=self.agent
        )
        agent_update = User.objects.create_user(
            username='BaseJournalSerializerTestCase_update'
        )
        object_update = DataLog.objects.get(id=1)
        object_update.data['message']['timestamp'] = (time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(time.time() + 86400)))
        object_update.data['message']['SystemSecurity'] = '$GALAXY_MAP_INFO_state_lawless;'
        serializer_update = BaseJournalSerializer(data=object_update.message)
        valid_update = serializer_update.is_valid()
        self.assertTrue(valid_update, serializer_update.errors)
        instance_update = serializer_update.save(
            created_by=agent_update,
            updated_by=agent_update
        )
        self.assertEqual(instance, instance_update)
        self.assertEqual(instance.created_by, instance_update.created_by)
        self.assertNotEqual(instance.updated_by, instance_update.updated_by)
        self.assertEqual(instance_update.updated_by, agent_update)
        self.assertEqual(instance.created_by, self.agent)

    def test_save(self):
        for item in DataLog.objects.all():
            serializer = BaseJournalSerializer(data=item.message)
            valid = serializer.is_valid()
            self.assertTrue(valid, serializer.errors)
            serializer.save(
                created_by=self.agent,
                updated_by=self.agent
            )

class FSDJumpSerializerTestCase(TestCase):

    fixtures = ['user', 'economy', 'system', 'body', 'bgs', 'exploration', 'material', 'mining', 'station','eddn_test_service_event_FSDJump']

    @classmethod
    def setUpTestData(cls):
        cls.agent = User.objects.create_user(
            username='FSDJumpSerializerTestCase'
        )

    def test_validate(self):
        for item in DataLog.objects.all():
            serializer = FSDJumpSerializer(data=item.message)
            valid = serializer.is_valid()
            self.assertTrue(valid, serializer.errors)

    def test_save(self):
        for item in DataLog.objects.all():
            serializer = FSDJumpSerializer(data=item.message)
            valid = serializer.is_valid()
            self.assertTrue(valid, serializer.errors)
            serializer.save(
                created_by=self.agent,
                updated_by=self.agent
            )

class DockedSerializerTestCase(TestCase):

    fixtures = ['user', 'economy', 'system', 'body', 'bgs', 'exploration', 'material', 'mining', 'station','eddn_test_service_event_Docked']

    @classmethod
    def setUpTestData(cls):
        cls.agent = User.objects.create_user(
            username='DockedSerializerTestCase'
        )

    def test_validate(self):
        for item in DataLog.objects.all():
            serializer = DockedSerializer(data=item.message)
            valid = serializer.is_valid()
            self.assertTrue(valid, serializer.errors)

    def test_save(self):
        for item in DataLog.objects.all():
            serializer = DockedSerializer(data=item.message)
            valid = serializer.is_valid()
            self.assertTrue(valid, serializer.errors)
            serializer.save(
                created_by=self.agent,
                updated_by=self.agent
            )

class BaseScanSerializerTestCase(TestCase):

    fixtures = ['user', 'economy', 'system', 'body', 'bgs', 'exploration', 'material', 'mining', 'station','eddn_test_service_event_Scan']

    @classmethod
    def setUpTestData(cls):
        cls.agent = User.objects.create_user(
            username='BaseScanSerializerTestCase'
        )

    def test_validate(self):
        for item in DataLog.objects.all():
            analysis = JournalAnalysis(item, self.agent)
            serializer = analysis.serializer_Scan()
            serializer = serializer(data=analysis.get_message())
            valid = serializer.is_valid()
            self.assertTrue(valid, serializer.errors)

    def test_save(self):
        for item in DataLog.objects.all():
            analysis = JournalAnalysis(item, self.agent)
            serializer = analysis.serializer_Scan()
            serializer = serializer(data=analysis.get_message())
            valid = serializer.is_valid()
            self.assertTrue(valid, serializer.errors)
            serializer.save(
                created_by=self.agent,
                updated_by=self.agent
            )

class LocationSerializerTestCase(TestCase):
    
    fixtures = ['user', 'economy', 'system', 'body', 'bgs', 'exploration', 'material', 'mining', 'station','eddn_test_service_event_Location']

    @classmethod
    def setUpTestData(cls):
        cls.agent = User.objects.create_user(
            username='LocationSerializerTestCase'
        )

    def test_validate(self):
        for item in DataLog.objects.all():
            serializer = LocationSerializer(data=item.message)
            valid = serializer.is_valid()
            self.assertTrue(valid, serializer.errors)

    def test_save(self):
        for item in DataLog.objects.all():
            serializer = LocationSerializer(data=item.message)
            valid = serializer.is_valid()
            self.assertTrue(valid, serializer.errors)
            serializer.save(
                created_by=self.agent,
                updated_by=self.agent
           )
            
class SAASignalsFoundSerializersTestCase(TestCase):
    
    fixtures = ['user', 'economy', 'system', 'body', 'bgs', 'exploration', 'material', 'mining', 'station','eddn_test_service_event_SAASignalsFound']

    @classmethod
    def setUpTestData(cls):
        cls.agent = User.objects.create_user(
            username='SAASignalsFoundSerializersTestCase'
        )

    def test_validate(self):
        for item in DataLog.objects.all():
            analysis = JournalAnalysis(item, self.agent)
            serializer = analysis.serializer_SAASignalsFound()
            serializer = serializer(data=analysis.get_message())
            valid = serializer.is_valid()
            self.assertTrue(valid, serializer.errors)

    def test_save(self):
        for item in DataLog.objects.all():
            analysis = JournalAnalysis(item, self.agent)
            serializer = analysis.serializer_SAASignalsFound()
            serializer = serializer(data=analysis.get_message())
            valid = serializer.is_valid()
            self.assertTrue(valid, serializer.errors)
            serializer.save(
                created_by=self.agent,
                updated_by=self.agent
            )

class CarrierJumpSerializerTestCase(TestCase):
    
    fixtures = ['user', 'economy', 'system', 'body', 'bgs', 'exploration', 'material', 'mining', 'station','eddn_test_service_event_CarrierJump']

    @classmethod
    def setUpTestData(cls):
        cls.agent = User.objects.create_user(
            username='CarrierJumpSerializerTestCase'
        )

    def test_validate(self):
        for item in DataLog.objects.all():
            serializer = CarrierJumpSerializer(data=item.message)
            valid = serializer.is_valid()
            self.assertTrue(valid, serializer.errors)

    def test_save(self):
        for item in DataLog.objects.all():
            serializer = CarrierJumpSerializer(data=item.message)
            valid = serializer.is_valid()
            self.assertTrue(valid, serializer.errors)
            serializer.save(
                created_by=self.agent,
                updated_by=self.agent
            )
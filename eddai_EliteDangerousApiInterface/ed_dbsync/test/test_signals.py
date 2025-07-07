from django.test import TestCase
from unittest.mock import MagicMock

from ed_dbsync.signals import update_social_account, remove_social_account
from users.models import User

from django_celery_beat.models import PeriodicTask
from ed_dbsync.tasks.capiJournalSync import CapiJournalSync

class EdDbsyncSignalsTestCase(TestCase):
    """
    Test case for Elite Dangerous DB sync signals
    """

    @property
    def get_tasck_name(self, user:User=None) -> str:
        if user is None:
            user:User = self.user
        return CapiJournalSync.get_task_name_for_periodic_task(user)

    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the test case
        """
        # Create a user and a social account for testing
        cls.user = User.objects.create(username='EdDbsyncSignalsTestCase')

    def test_update_social_account(self):
        
        sociallogin_mock = MagicMock()
        sociallogin_mock.provider = 'frontier'
        sociallogin_mock.user = self.user

        update_social_account(sender=None, request=None, sociallogin=sociallogin_mock)

        # Check if the periodic task was created or updated
        exists_periodic_task = PeriodicTask.objects.filter(name=self.get_tasck_name).exists()
        self.assertTrue(exists_periodic_task, f"Periodic task '{self.get_tasck_name}' should not exist")

    def test_remove_social_account(self):

        sociallogin_mock = MagicMock()
        sociallogin_mock.provider = 'frontier'
        sociallogin_mock.user = self.user

        # Create the periodic task first
        update_social_account(sender=None, request=None, sociallogin=sociallogin_mock)

        # Now remove the social account
        remove_social_account(sender=None, request=None, socialaccount=sociallogin_mock)

        # Check if the periodic task was deleted
        exists_periodic_task = PeriodicTask.objects.filter(name=self.get_tasck_name).exists()
        self.assertFalse(exists_periodic_task, f"Periodic task '{self.get_tasck_name}' should exist")
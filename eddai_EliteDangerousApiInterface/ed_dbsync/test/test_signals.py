from django.test import TestCase
from unittest.mock import MagicMock, patch

from ed_dbsync.signals import (
    handle_social_account_update, handle_social_account_removal,
    handle_user_deletion, setup_capi_on_signup
)
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

    def test_handle_social_account_update(self):
        
        sociallogin_mock = MagicMock()
        sociallogin_mock.account = MagicMock()
        sociallogin_mock.account.provider = 'frontier'
        sociallogin_mock.user = self.user

        handle_social_account_update(sender=None, request=None, sociallogin=sociallogin_mock)

        # Check if the periodic task was created or updated
        exists_periodic_task = PeriodicTask.objects.filter(name=self.get_tasck_name).exists()
        self.assertTrue(exists_periodic_task, f"Periodic task '{self.get_tasck_name}' should not exist")

    def test_handle_social_account_removal(self):

        socialaccount_mock = MagicMock()
        socialaccount_mock.account = MagicMock()
        socialaccount_mock.account.provider = 'frontier'
        socialaccount_mock.user = self.user

        handle_social_account_removal(sender=None, request=None, socialaccount=socialaccount_mock)

        # Check if the periodic task was deleted
        exists_periodic_task = PeriodicTask.objects.filter(name=self.get_tasck_name).exists()
        self.assertFalse(exists_periodic_task, f"Periodic task '{self.get_tasck_name}' should not exist after removal")

    def test_handle_user_deletion(self):

        handle_user_deletion(sender=None, instance=self.user)

        # Check if the periodic task was deleted
        exists_periodic_task = PeriodicTask.objects.filter(name=self.get_tasck_name).exists()
        self.assertFalse(exists_periodic_task, f"Periodic task '{self.get_tasck_name}' should not exist after user deletion")
from django.test import TestCase
from unittest.mock import patch, MagicMock

from users.signals import update_cmdr_profile, update_cmdr_profile_on_connect
from users.models import User
from allauth.socialaccount.models import SocialAccount

class UserSignalsTestCase(TestCase):
    """
    Test case for user signals
    """
    
    @classmethod
    def setUpTestData(cls):
        """
        Set up test data for the test case
        """
        # Create a user and a social account for testing
        cls.user = User.objects.create(username='UserSignalsTestCase')
        cls.social_account = SocialAccount.objects.create(
            user=cls.user,
            provider='frontier',
        )

    def setUp(self):
        """
        Set up the test case environment
        """
        self.user.username = 'UserSignalsTestCase'
        self.user.save()

    @patch('users.signals.get_cmdr_name')
    def test_update_cmdr_profile(self, mock_get_cmdr_name):
        """
        Test the update_cmdr_profile signal handler
        """
        # Configura il mock per restituire un nome specifico
        mock_get_cmdr_name.return_value = 'fabbietto01'
        
        self.assertEqual(self.user.username, 'UserSignalsTestCase')
        
        # Call the signal handler directly
        update_cmdr_profile(sender=None, user=self.user)

        # Verifica che get_cmdr_name sia stato chiamato
        mock_get_cmdr_name.assert_called_once_with(self.user)
        
        # Ricarica l'utente dal database
        self.user.refresh_from_db()
        
        # Check if the user's username has been updated correctly
        self.assertEqual(self.user.username, 'fabbietto01')

    @patch('users.signals.get_cmdr_name')
    def test_update_cmdr_profile_on_connect(self, mock_get_cmdr_name):
        """
        Test the update_cmdr_profile_on_connect signal handler
        """
        # Configura il mock per restituire un nome specifico
        mock_get_cmdr_name.return_value = 'fabbietto01'
        
        # Create a mock SocialLogin object
        mock_sociallogin = MagicMock()
        mock_sociallogin.user = self.user
        mock_sociallogin.account = MagicMock()
        mock_sociallogin.account.provider = 'frontier'

        self.assertEqual(self.user.username, 'UserSignalsTestCase')

        # Call the signal handler directly
        update_cmdr_profile_on_connect(sender=None, request=None, sociallogin=mock_sociallogin)

        # Verifica che get_cmdr_name sia stato chiamato
        mock_get_cmdr_name.assert_called_once_with(self.user)

        # Ricarica l'utente dal database
        self.user.refresh_from_db()

        # Check if the user's username has been updated correctly
        self.assertEqual(self.user.username, 'fabbietto01')
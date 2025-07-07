from django.test import TestCase
from unittest.mock import patch, MagicMock

from users.signals import update_cmdr_profile
from users.models import User

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

    @patch('users.signals.get_cmdr_name')
    def test_update_cmdr_profile(self, mock_get_cmdr_name):
        """
        Test the update_cmdr_profile signal handler
        """
        # Configura il mock per restituire un nome specifico
        mock_get_cmdr_name.return_value = 'fabbietto01'
        
        # Crea un oggetto sociallogin mock
        sociallogin_mock = MagicMock()
        sociallogin_mock.account = MagicMock()
        sociallogin_mock.account.provider = 'frontier'
        sociallogin_mock.user = self.user

        self.assertEqual(self.user.username, 'UserSignalsTestCase')
        
        # Call the signal handler directly
        update_cmdr_profile(sender=None, request=None, sociallogin=sociallogin_mock)

        # Verifica che get_cmdr_name sia stato chiamato
        mock_get_cmdr_name.assert_called_once_with(self.user)
        
        # Ricarica l'utente dal database
        self.user.refresh_from_db()
        
        # Check if the user's username has been updated correctly
        self.assertEqual(self.user.username, 'fabbietto01')
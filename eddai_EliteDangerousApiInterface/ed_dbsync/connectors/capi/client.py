import logging
import requests
from datetime import datetime
import json
from django.conf import settings

from allauth.socialaccount.models import SocialToken, SocialApp
from allauth.socialaccount.providers.oauth2 import client
from users.models import User

from .exceptions import (
    CapiClientError, CapiClinetAuthError, FleetCarrierNotOwnedError, CapiClinetRequestError,
    JournalNoContentError, JournalPartialContentError
)

# Logger moved outside the class
log = logging.getLogger('capi')

class CapiClient:
    """
    CapiClient is a client for connecting to the CAPI broker and receiving messages.

    Attributes:
        host (str): URL of the CAPI broker.
        agent (User): User agent for sending data.

    Methods:
        connect(endpoint): Connects to the specified CAPI endpoint and returns data.
    """
    host = settings.CAPI_HOST

    @property
    def endpoint_methods(self):
        """
        Returns a dictionary of endpoint methods for the CAPI client.
        
        This property is used to map endpoint names to their corresponding methods.
        """
        return {
            'journal': self.get_journal,
            'profile': self.get_profile,
            'fleetcarrier': self.get_fleetcarrier,
        }

    def __init__(self, agent: User):
        self.agent: User = agent

    @classmethod
    def from_task(cls, user: User):
        """
        Creates a CapiClient instance from a user.

        Args:
            user (User): The user to create the CapiClient for.

        Returns:
            CapiClient: An instance of CapiClient.
        """
        return cls(agent=user)

    def get_social_app(self) -> SocialApp:
        """
        Retrieves the SocialApp for the CAPI client.

        Returns:
            SocialApp: The SocialApp associated with the CAPI client.
        """
        try:
            return SocialApp.objects.get(name='Frointer')
        except SocialApp.DoesNotExist:
            raise CapiClinetAuthError("SocialApp 'Frointer' does not exist. Please create it in the admin panel.")

    def get_social_token(self) -> SocialToken:
        """
        Retrieves the SocialToken for the CAPI client.

        Returns:
            SocialToken: The SocialToken associated with the CAPI client.
        """
        try:
            return SocialToken.objects.get(app=self.get_social_app(), account__user=self.agent)
        except SocialToken.DoesNotExist:
            raise CapiClinetAuthError(f"SocialToken for user {self.agent.username} does not exist. Please authenticate the user with CAPI.")

    def get_token(self) -> str:
        return self.get_social_token().token

    def get_request(self, path: str) -> requests.Response:
        """
        Executes a GET request to the CAPI API.

        Args:
            path (str): The endpoint path to call.

        Returns:
            requests.Response: The HTTP response.
        """
        return requests.get(
            f"https://{self.host}/{path}",
            headers={
                'Authorization': f'Bearer {self.get_token()}',
                'User-Agent': settings.CAPI_USER_AGENT
            }
        )

    def get_journal(self, *arg, **kwargs) -> list[dict]:
        """
        Retrieves the journal data from the CAPI broker.
        Args:
            *arg: Additional positional arguments.
            **kwargs: Additional keyword arguments, including 'date' in 'YYYY/MM/DD' format
        Returns:
            list[dict]: A list of journal entries from the CAPI broker.
        """
        path = 'journal'
        date = kwargs.get('date', None)
        if date:
            # Validate date format
            try:
                datetime.strptime(date, '%Y/%m/%d')
                path += f'/{date}'
            except ValueError:
                raise CapiClientError(f"Invalid date format: {date}. Use YYYY/MM/DD format")
        
        try:
            response = self.get_request(path)

            response.raise_for_status()

            if response.status_code == 204:
                raise JournalNoContentError("No content in journal response (204 No Content). This may mean the player has not played this day.")
            if response.status_code == 206:
                raise JournalPartialContentError("Partial content in journal response (206 Partial Content). This may mean the request did not get the entire journal.")

            response_text = response.text.strip()

            if not response_text:
                return []
            
            response_json = []
            for line in response_text.splitlines():
                line = line.strip()
                if line:
                    try:
                        entry = json.loads(line)
                        response_json.append(entry)
                    except json.JSONDecodeError as line_error:
                        log.warning(
                            f"Could not parse journal line: {repr(line)}",
                            exc_info=True,
                            extra={
                                'line_content': repr(line),
                                'user_id': self.agent.id,
                            }
                        )
                        continue
            return response_json
        except requests.RequestException as e:
            if e.response.status_code == 401:
                raise CapiClinetAuthError("Authentication error: Invalid or expired token.")
            else:
                raise CapiClinetRequestError(f"Error in journal request") from e
        except JournalNoContentError as e:
            raise e
        except JournalPartialContentError as e:
            raise e
        except Exception as e:
            raise CapiClientError(f"Unexpected error in journal request") from e

    def get_profile(self, *arg, **kwargs) -> dict:
        """
        Retrieves the profile data from the CAPI broker.

        Returns:
            dict: The profile data from the CAPI broker.
            
        Raises:
            CapiClientError: In case of request error.
        """
        try:
            response = self.get_request('profile')
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            raise CapiClientError(f"Error in profile request") from e

    def get_fleetcarrier(self, *arg, **kwargs) -> dict:
        """
        Retrieves the fleet carrier data from the CAPI broker.

        Returns:
            dict: The fleet carrier data from the CAPI broker.
            
        Raises:
            FleetCarrierNotOwnedError: If user doesn't own a Fleet Carrier (status 204).
            CapiClientError: In case of other request errors.
        """
        try:
            response = self.get_request('fleetcarrier')
            
            if response.status_code == 204:
                raise FleetCarrierNotOwnedError("You don't own a Fleet Carrier")
            
            response.raise_for_status()
            return response.json()
        except FleetCarrierNotOwnedError as e:
            raise e
        except requests.RequestException as e:
            raise CapiClientError(f"Error in fleetcarrier request") from e
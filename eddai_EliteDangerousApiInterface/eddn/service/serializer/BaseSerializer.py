from typing import Callable
from datetime import datetime

from django.conf import settings
from django.core.cache import cache
from django.contrib.auth import authenticate

from rest_framework import serializers

from users.models import User

class BaseSerializer(serializers.Serializer):

    _agent = None

    @property
    def agent(self) -> User:
        """
        restituisce l'utente utilizzato per inviare il datto
        """
        if not self._agent:
            self._agent = self.get_user_agent()
        return self._agent

    def save(self, **kwargs):
        assert hasattr(self, '_errors'), (
            'You must call `.is_valid()` before calling `.save()`.'
        )

        assert not self.errors, (
            'You cannot call `.save()` on a serializer with invalid data.'
        )

        # Guard against incorrect use of `serializer.save(commit=False)`
        assert 'commit' not in kwargs, (
            "'commit' is not a valid keyword argument to the 'save()' method. "
            "If you need to access data before committing to the database then "
            "inspect 'serializer.validated_data' instead. "
            "You can also pass additional keyword arguments to 'save()' if you "
            "need to set extra attributes on the saved model instance. "
            "For example: 'serializer.save(owner=request.user)'.'"
        )

        assert not hasattr(self, '_data'), (
            "You cannot call `.save()` after accessing `serializer.data`."
            "If you need to access data before committing to the database then "
            "inspect 'serializer.validated_data' instead. "
        )

        validated_data = {**self.validated_data, **kwargs}

        self.instance = self.update_or_create(validated_data)
        assert self.instance is not None, (
            '`update_or_create()` did not return an object instance.'
        )

        return self.instance

    def update_or_create(self, validated_data:dict):
        """
        metodo chiammato da save(), utilizatto per creare o aggiornare le istanze passate
        da senvizio di eddn
        """
        raise NotImplementedError('`update_or_create()` must be implemented.')

    def set_data_defaults(self, validated_data:dict) -> dict:
        """
        utiliza questo metodo per definire i datti di default utilizatti per creare se non presente
        una istanza, questo medodo vine chiamato da  get_data_defaults()
        """
        raise NotImplementedError('`set_data_defaults()` must be implemented.')
    
    def set_data_defaults_create(self, validated_data:dict) -> dict:
        """
        utiliza questo metodo per definire i datti di default utilizatti per creare se non presente
        una istanza, questo medodo vine chiamato da  get_data_defaults_create()
        """
        raise NotImplementedError('`set_data_defaults_create()` must be implemented.')
    
    def set_data_defaults_update(self, validated_data:dict) -> dict:
        """
        utiliza questo metodo per definire i datti di default utilizatti per aggiornare se presente
        una istanza, questo medodo vine chiamato da  get_data_defaults_update()
        """
        raise NotImplementedError('`set_data_defaults_update()` must be implemented.')

    def data_preparation(self, validated_data:dict) -> dict:
        """
        questo metodo viene chiamato da save() per preparare i dati da salvare
        """
        raise NotImplementedError('`data_preparation()` must be implemented.')
    
    def _clean_data_defaults(self, default_data:dict) -> dict:
        """
        ripulisce i datti di default togniaendo i datti che sono impostatti su none
        """
        for key, value in list(default_data.items()):
            if value == None:
                del default_data[key]
        return default_data

    def _get_data_defaults(self, validated_data:dict, function:Callable[[dict], dict]) -> dict:
        default_data = function(validated_data)
        default_data = self._clean_data_defaults(default_data)
        return default_data
    
    def get_data_defaults(self, validated_data:dict, function:Callable[[dict], dict]=None) -> dict:
            """
            Returns the data with default values applied.

            Args:
                validated_data (dict): The validated data.
                function (function, optional): The function to set default values. Defaults to None.

            Returns:
                dict: The data with default values applied.
            """
            if not function:
                function = self.set_data_defaults
            return self._get_data_defaults(validated_data, function)

    def get_data_defaults_create(self, *args, **kwargs) -> dict:
        """
        Returns a dictionary containing default data for creating a new object.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
                validated_data (dict): The validated data for creating the object.
                function (function): The function to set data defaults.

        Returns:
            dict: A dictionary containing default data for creating a new object.
        """
        validated_data: dict = kwargs.get('validated_data', None)
        if validated_data:
            var_function:Callable[[dict], dict] = kwargs.get('function', None)
            if not var_function:
                var_function = self.set_data_defaults_create
            return self._get_data_defaults(validated_data, var_function)
        return {
            'created_by': self.agent,
            'updated_by': self.agent
        }
    
    def get_data_defaults_update(self, *args, **kwargs) -> dict:
        """
        Returns a dictionary containing default data for updating records.

        Args:
            *args: Variable length argument list.
            **kwargs: Arbitrary keyword arguments.
                validated_data (dict): The validated data to be updated.
                function (function): The function to be used for setting data defaults.

        Returns:
            dict: A dictionary containing default data for updating records.

        """
        validated_data: dict = kwargs.get('validated_data', None)
        if validated_data:
            var_function: Callable[[dict], dict] = kwargs.get('function', None)
            if not var_function:
                var_function = self.set_data_defaults_update
            return self._get_data_defaults(validated_data, var_function)
        return {
            'updated_by': self.agent
        }

    def get_time(self, validated_data:dict = None) -> datetime:
        """
        restituisce il giorno e ora in qui e stato inviato il datto da eddn
        """
        if validated_data:
            return validated_data.get('timestamp')
        return self.validated_data.get('timestamp')

    @staticmethod
    def get_user_agent() -> User:
        """
        restituisce il user agent utilizzato per inviare il datto
        """
        user = cache.get_or_set(
            settings.EDDN_USER_AGENT_CACHE_KEY,
            lambda: authenticate(
                username=settings.EDDN_USER_NAME_AGENT,
                password=settings.EDDN_USER_PASSWORD_AGENT
            )
        )
        if isinstance(user, User):
            return user
        raise ValueError('User not found')

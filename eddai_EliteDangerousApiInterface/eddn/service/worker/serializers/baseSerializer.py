from typing import Callable
from datetime import datetime

from rest_framework import serializers

class BaseSerializer(serializers.Serializer):

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
        method called by save(), used to create or update instances passed
        by the eddn service
        """
        raise NotImplementedError('`update_or_create()` must be implemented.')

    def set_data_defaults(self, validated_data:dict) -> dict:
        """
        use this method to define the default data used to create an instance if not present,
        this method is called by get_data_defaults()
        """
        raise NotImplementedError('`set_data_defaults()` must be implemented.')
    
    def set_data_defaults_create(self, validated_data:dict) -> dict:
        """
        use this method to define the default data used to create an instance if not present,
        this method is called by get_data_defaults_create()
        """
        raise NotImplementedError('`set_data_defaults_create()` must be implemented.')
    
    def set_data_defaults_update(self, validated_data:dict) -> dict:
        """
        use this method to define the default data used to update an instance if present,
        this method is called by get_data_defaults_update()
        """
        raise NotImplementedError('`set_data_defaults_update()` must be implemented.')
    
    def _clean_data_defaults(self, default_data:dict) -> dict:
        """
        cleans the default data by removing the data that is set to none
        """
        for key, value in list(default_data.items()):
            if value == None:
                del default_data[key]
        return default_data

    def _get_data_defaults(self, validated_data:dict, function:Callable[[dict], dict], *args, **kwargs) -> dict:
        """
        Processes the validated data through a given function and cleans the resulting default data.
        Args:
            validated_data (dict): The data that has been validated.
            function (Callable[[dict], dict]): A function that takes the validated data and returns a dictionary of default data.
        Returns:
            dict: The cleaned default data.
        """
        default_data = function(validated_data)
        default_data = {**default_data, **kwargs}
        default_data = self._clean_data_defaults(default_data)
        return default_data
    
    def get_data_defaults(self, validated_data:dict, function:Callable[[dict], dict]=None, *args, **kwargs) -> dict:
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
            return self._get_data_defaults(validated_data, function, *args, **kwargs)

    def get_data_defaults_create(self, validated_data, function:Callable[[dict], dict]=None, *args, **kwargs) -> dict:
        """
        Returns a dictionary containing default data for creating a new object.

        Args:
            validated_data (dict): The validated data to be updated.
            function (function): The function to be used for setting data defaults.

        Returns:
            dict: A dictionary containing default data for creating a new object.
        """
        if not function:
            function = self.set_data_defaults_create
        return self._get_data_defaults(validated_data, function, *args, **kwargs)

    def get_data_defaults_update(self, validated_data, function:Callable[[dict], dict]=None, *args, **kwargs) -> dict:
        """
        Returns a dictionary containing default data for updating records.

        Args:
            validated_data (dict): The validated data to be updated.
            function (function): The function to be used for setting data defaults.

        Returns:
            dict: A dictionary containing default data for updating records.

        """
        if not function:
            function = self.set_data_defaults_update
        return self._get_data_defaults(validated_data, function, *args, **kwargs)

    def get_time(self, validated_data:dict = None) -> datetime:
        """
        returns the date and time when the data was sent by eddn
        """
        if validated_data:
            return validated_data.get('updated_at')
        return self.validated_data.get('updated_at')
    
    def create_dipendent(self, instance, validated_data:dict):
        """
        Creates dependencies for the newly created instance.
        Args:
            instance: The instance for which dependencies are to be created.
            validated_data (dict): The validated data used to create dependencies.
        Raises:
            NotImplementedError: This method should be implemented by subclasses.
        """
        
        raise NotImplementedError

    def update_dipendent(self, instance, validated_data:dict):
        """
        Update the dependent attributes of the given instance with the provided validated data.
        This function is intended to be used for updating the dependencies of the created instance.
        Args:
            instance: The instance whose dependent attributes need to be updated.
            validated_data (dict): A dictionary containing the validated data to update the instance with.
        Raises:
            NotImplementedError: This method should be implemented by subclasses.
        """
        raise NotImplementedError
from rest_framework import serializers
from datetime import datetime

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

    def data_preparation(self, validated_data:dict) -> dict:
        """
        questo metodo viene chiamato da save() per preparare i dati da salvare
        """
        raise NotImplementedError('`data_preparation()` must be implemented.')
    
    def clean_data_defaults(self, default_data:dict) -> dict:
        """
        ripulisce i datti di default togniaendo i datti che sono impostatti su none
        """
        for key, value in list(default_data.items()):
            if value == None:
                del default_data[key]
        return default_data

    def get_data_defaults(self, validated_data:dict, fuction=None) -> dict:
        """
        chiama questo medodo per restituire i default data
        """
        if fuction:
            default_data = fuction(validated_data)
        else: 
            default_data = self.set_data_defaults(validated_data)
        default_data = self.clean_data_defaults(default_data)
        return default_data

    def get_time(self, validated_data:dict = None) -> datetime:
        """
        restituisce il giorno e ora in qui e stato inviato il datto da eddn
        """
        if validated_data:
            return validated_data.get('timestamp')
        return self.validated_data.get('timestamp')


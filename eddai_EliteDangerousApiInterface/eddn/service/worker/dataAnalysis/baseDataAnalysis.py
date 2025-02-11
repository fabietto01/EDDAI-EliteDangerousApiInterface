import logging
from rest_framework.serializers import Serializer

from .errors import NotDataContentError
from eddn.models import DataLog
from users.models import User

class BaseDataAnalysis:

    log = logging.getLogger("eddn")

    def __init__(self, istance:DataLog, agent:User, *args, **kwargs):
        self.istance = istance
        self.agent = agent

    def get_serializer_class(self) -> Serializer:
        raise NotImplementedError('`get_serializer_class()` must be implemented.')
    
    def get_serializer(self, *args, **kwargs) -> Serializer:
        """
        Return the serializer instance that should be used for validating and
        deserializing input, and for serializing output.
        """
        serializer_class = self.get_serializer_class()
        return serializer_class(*args, **kwargs)

    def get_message(self) -> dict:
        """
        Return the message inside the data stored in the class
        """
        data = self.istance.data
        if not data:
            raise NotDataContentError("data not found")
        return data.get("message")

    def run_analysis(self):
        serializer = self.get_serializer(data=self.get_message())
        self.istance.save()
        if serializer.is_valid():
            serializer.save(
                created_by=self.agent,
                updated_by=self.agent
            )
        # else:
        #     self.log.error(f"error validating '{self.istance.schema}': {serializer.errors}")
        #     self.istance.error = serializer.errors
        
        return self.istance
import logging
from rest_framework.serializers import Serializer, ValidationError

from .errors import NotDataContentError, NotSerializerError
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
        try:
            serializer = self.get_serializer(data=self.get_message())
            serializer.is_valid(raise_exception=True)
            serializer.save(
                created_by=self.agent,
                updated_by=self.agent
            )
            self.istance.error = None
        except ValidationError as e:
            self.log.error(f"error validating '{self.istance.pk}': {serializer.errors}")
            self.istance.error = serializer.errors
            self.istance.save()
        except NotSerializerError as e:
            self.log.debug(f"error in data analysis '{self.istance.pk}': {e}")
            self.istance.error = {"error": f"{e}"}
            self.istance.save()
        except Exception as e:
            self.log.exception(f"generic error in data analysis '{self.istance.pk}': {e}")
            self.istance.error = {"error": f"{e}"}
            self.istance.save()
        return self.istance
from celery.utils.log import get_task_logger
from rest_framework.serializers import Serializer, ValidationError

from ed_dbsync.analysts.exception import NotSerializerError, NotDataContentError
from ed_dbsync.dataclass import IncomingData

log = get_task_logger(__name__)

class BaseDataAnalyst:
    """
    Base class for data analysts.
    This class provides a common interface for data analysts to implement their specific analysis logic.
    """
    def __init__(self, istance:IncomingData, agent, *args, **kwargs):
        """
        Initialize the BaseDataAnalyst with an istance and an agent.
        
        :param istance: The data istance to be analyzed.
        :param agent: The user agent performing the analysis.
        """
        self.istance = istance
        self.agent = agent

    def get_serializer_class(self) -> Serializer:
        raise NotImplementedError('`get_serializer_class()` must be implemented.')
    
    def get_serializer(self, *args, **kwargs) -> Serializer:
        """
        Return the serializer istance that should be used for validating and
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
        if self.istance.source == 'capi_api':
            return data
        elif self.istance.source == 'eddn':
            return data.get("message", {})
        raise NotImplementedError("`get_message()` must be implemented for the specific source type.")

    def run_analysis(self):
        """
        Run the analysis on the provided istance.
        
        This method should be implemented by subclasses to perform specific analysis logic.
        """
        log.info(
            f"Start of data analysis.", 
            extra={
                'istance_id': self.istance.guid,
                'analyst_class_name': self.__class__.__name__,
                'agent_id': self.agent.id
            }
        )
        try:
            serializer = self.get_serializer(data=self.get_message())
            serializer.is_valid(raise_exception=True)
            serializer.save(
                created_by=self.agent,
                updated_by=self.agent
            )
        except NotSerializerError as e:
            log.debug(
                "An appropriate serializer was not found.", 
                exc_info=e, 
                extra={
                    'istance_id': self.istance.guid,
                    'analyst_class_name': self.__class__.__name__,
                    'agent_id': self.agent.id,
                    'instance': self.istance,
                }
            )
        else:
            log.info(
                "Data analysis completed successfully. ", 
                extra={
                    'istance_id': self.istance.guid,
                    'analyst_class_name': self.__class__.__name__,
                    'agent_id': self.agent.id,
                    'instance': self.istance,
                }
            )
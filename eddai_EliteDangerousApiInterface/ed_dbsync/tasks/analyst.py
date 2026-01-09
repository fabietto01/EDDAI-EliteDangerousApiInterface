from celery import  Task
from celery.utils.log import get_task_logger

from .exception import NotSourceError
from rest_framework.serializers import ValidationError

from users.models import User
from ed_dbsync.dataclass import IncomingData

from ed_dbsync.analysts.base import BaseDataAnalyst
from ed_dbsync.analysts import JournalAnalyst, Commodity3Analyst

log = get_task_logger(__name__)

class AnalystTasck(Task):
    """
    Questo task si occupa di analizzare i dati ricevuti da EDDN o CAPI API.
    Si basa sul tipo di sorgente per determinare quale analisi eseguire.
    Può essere esteso per supportare ulteriori sorgenti in futuro.
    Attributes:
        name (str): Il nome del task.
        ignore_result (bool): Indica se il risultato del task deve essere ignorato.
        max_retries (int): Numero massimo di tentativi di esecuzione del task in caso di errore.
        default_retry_delay (int): Ritardo predefinito tra i tentativi di esecuzione del task.
        log (Logger): Il logger per registrare i messaggi di log.
    """

    name = 'ed_dbsync.tasks.AnalystTasck'
    ignore_result = True

    max_retries = 5
    retry_backoff = 60*60*4
    retry_backoff_max = 60*60*5
    autoretry_for = (ValidationError,)

    def get_analyst_class(self, istance) -> BaseDataAnalyst:
        try:
            func = getattr(self, f"analyst_{istance.source}")
        except AttributeError as e:
            raise NotSourceError(istance.source) from e
        else:
            return func(istance=istance)

    def get_analyst(self, istance, *args, **kwargs) -> BaseDataAnalyst:
        analyst_class = self.get_analyst_class(istance)
        return analyst_class(istance=istance, *args, **kwargs)
        
    def analyst_eddn(self, istance:IncomingData):
        if istance.data["$schemaRef"] == "https://eddn.edcd.io/schemas/journal/1":
            return JournalAnalyst
        elif istance.data["$schemaRef"] == "https://eddn.edcd.io/schemas/commodity/3":
            return Commodity3Analyst
        else:
            raise NotSourceError(f"Unsupported EDDN schemaRef: {istance.data['$schemaRef']}")

    def analyst_capi_api(self, istance:IncomingData):
        raise NotImplementedError(
            "The service has not yet implemented the EDDN analyst. "
            "Please implement the 'run_eddn' method in the AnalystTasck class."
        )

    def run(self, *args, **kwargs):
        """
        Run the analysis based on the source of the data.
        """
        istance:IncomingData = kwargs.get('istance')
        agent:User = kwargs.get('agent')
        log.info(
            f"Start search for apropiate analyst", 
            extra={
                'istance_id': istance.guid,
                'istance_source':istance.source
            }
        )
        try:
            analyst = self.get_analyst(istance=istance, agent=agent)
            analyst.run_analysis()
            log.info(
                f"Analysis completed from {analyst.__class__.__name__}", 
                extra={
                    'istance_id': istance.guid,
                    'istance_source':istance.source,
                    'analyst_class_name': analyst.__class__.__name__
                }
            )
        except NotSourceError as e:
            log.error(
                f"No analyst was found for the data source", 
                exc_info=True, extra={
                    'istance_id': istance.guid, 'instance': istance,
                    'istance_source':istance.source
                }
            )
        except ValidationError as e:
            log.error(
                f"Validation error during analysis:", 
                exc_info=True, extra={
                    'istance_id': istance.guid, 'instance': istance,
                    'istance_source':istance.source,
                    'analyst_class_name': analyst.__class__.__name__
                }
            )
            raise e
        except Exception as e:
            log.error(
                f"An error occurred during analysis", 
                exc_info=True, extra={
                    'istance_id': istance.guid, 'instance': istance,
                    'istance_source':istance.source
                }
            )
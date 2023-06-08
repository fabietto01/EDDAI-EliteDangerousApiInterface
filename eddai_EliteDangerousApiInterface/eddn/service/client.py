from django.conf import settings
import zlib, zmq, json
from eddn.models import DataLog
from celery import Task
from celery.utils.log import get_task_logger
from eddn.service.dataAnalytics.utility import star_analytic

class EddnClient(Task):

    __log = get_task_logger(__name__)
    __debug = settings.DEBUG
    __timeout = settings.EDDN_TIMEOUT
    __rely = settings.EDDN_RELY
    __authori_softwers = settings.AUTHORI_SED_SOFTWARS
    name="ServiceEDDN"
    
    #https://docs.celeryq.dev/en/stable/userguide/tasks.html#retrying
    autoretry_for = (Exception,)
    max_retries = None
    retry_backoff = 5
    retry_backoff_max = 30
    retry_jitter = True

    time_limit=None
    ignore_result = True

    def run(self, *args, **kwargs):
        self.connect()

    def on_retry(self, *args, **kwargs):
        self.__log.info(f"Retry in max {self.retry_backoff_max} seconds...")

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        self.__log.critical(f"Failed to EDDN: %s", exc , exc_info=True) #exc_info=True

    def connect(self):
        """
        istanza la classe zmq.Context(), creando il socket 'zmq.SUB'
        """
        self.__log.info("Create a Socket associated with this Context")
        context = zmq.Context()
        subscriber = context.socket(zmq.SUB)
        subscriber.setsockopt(zmq.SUBSCRIBE, b"")
        subscriber.setsockopt(zmq.RCVTIMEO, self.__timeout)
        self.__log.info("created a socket")
        while True:
            try:
                subscriber.connect(self.__rely)
                self.__log.info("Connecting to EDDN")
                self.receive(subscriber)
                self.__log.error(f"Disconecter from {self.__rely}")
            except zmq.ZMQError as e:
                subscriber.disconnect(self.__rely)
                self.__log.critical(f"Failed to connecting EDDN broker: %s", e, exc_info=True)

    def receive(self, subscriber:zmq.Socket):
        """
        al interno di un ciclo while resta in atesta di un messagio dall
        broker EDDN, per poi inoltrare il messagio alla funzione process()
        """
        while True:
            dataCompres = subscriber.recv()
            if dataCompres == False:
                self.__log.error(f"The connection was lost From {self.__rely}")
                break

            dataDeCompress = zlib.decompress(dataCompres)
            if dataDeCompress == False:
                self.__log.error(f"Failed to decompress message")
            
            dataJson = json.loads(dataDeCompress)
            if dataJson == False:
                self.__log.error(f"Failed to decode message")
            
            if dataJson['header']['softwareName'] in self.__authori_softwers:
                self.__log.debug(f"Received message from EDDN broker: {dataJson}")
                istance = DataLog(data=dataJson)
                star_analytic(istance)
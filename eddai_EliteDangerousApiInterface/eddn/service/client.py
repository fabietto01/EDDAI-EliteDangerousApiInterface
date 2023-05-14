from django.conf import settings
import zlib, zmq, json, logging
import time
from eddn.models import DataLog
from celery import Task

from eddn.service.dataAnalytics.JournalAnalytics import JournalAnalytic
from eddn.service.dataAnalytics.Commodity3 import Commodity3Analytic

def process(istance:DataLog) -> DataLog:
    if istance.data["$schemaRef"] == "https://eddn.edcd.io/schemas/journal/1":
        analytic = JournalAnalytic(istance=istance)
        istance = analytic.analyst()
    elif istance.data["$schemaRef"] == "https://eddn.edcd.io/schemas/commodity/3":
        analytic = Commodity3Analytic(istance=istance)
        istance = analytic.analyst()
    return istance

class EddnClient(Task):

    __log = logging.getLogger("django")
    __debug = settings.DEBUG
    __timeout = settings.EDDN_TIMEOUT
    __rely = settings.EDDN_RELY
    __authori_softwers = settings.AUTHORI_SED_SOFTWARS
    name="ServiceEDN"
    retry=True
    ignore_result=True
    default_retry_delay=30
    time_limit=0

    def run(self, *args, **kwargs):
        self.connect()

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        self.__log.critical(f"Failed to EDDN: %s", exc , exc_info=True)
        self.__log.info(f"Retry in 5 seconds...")

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        self.__log.info(f"on_failure")

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
                process(istance)
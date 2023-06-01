from django.conf import settings
import zlib, zmq, json, logging
from eddn.models import DataLog
from celery import Task

from eddn.service.dataAnalytics import JournalAnalytic,  Commodity3Analytic

def process(istance:DataLog) -> DataLog:
    if istance.data["$schemaRef"] == "https://eddn.edcd.io/schemas/journal/1":
        analytic = JournalAnalytic(istance=istance)
        istance = analytic.analyst()
    elif istance.data["$schemaRef"] == "https://eddn.edcd.io/schemas/commodity/3":
        analytic = Commodity3Analytic(istance=istance)
        istance = analytic.analyst()
    return istance

import time

class EddnClient(Task):

    def __init__(self) -> None:
        super().__init__()


    __log = logging.getLogger("django")
    __debug = settings.DEBUG
    __timeout = settings.EDDN_TIMEOUT
    __rely = settings.EDDN_RELY
    __authori_softwers = settings.AUTHORI_SED_SOFTWARS
    name="ServiceEDDN"
    max_retries = None
    default_retry_delay=30
    ignore_result=True
    time_limit=None

    def run(self, *args, **kwargs):
        self.test()

    def on_retry(self, exc, task_id, args, kwargs, einfo):
        self.__log.critical(f"Failed to EDDN: %s", exc , exc_info=True)
        self.__log.info(f"Retry in 5 seconds...")

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        self.__log.info(f"on_failure")

    def test(self):
        time.sleep(2)
        1/0

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
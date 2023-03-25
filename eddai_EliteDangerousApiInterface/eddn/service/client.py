import json
from django.conf import settings
import zlib, zmq, simplejson, logging
import time

from eddn.service.dataAnalytics.JournalAnalytics import JournalAnalytic

class EddnClient(object):

    __log = logging.getLogger("django")
    __debug = settings.DEBUG
    __timeout = settings.EDDN_TIMEOUT
    __rely = settings.EDDN_RELY
    __authori_softwers = settings.AUTHORI_SED_SOFTWARS
    __start = True

    def start(self):
        while (self.__debug == False) or self.__start:
            self.__start = False
            try:
                self.connect()
            except Exception as e:
                self.__log.critical(f"Failed to EDDN: {e}" + (" \nRetrying in 5 seconds..." if self.__debug else ""))
                time.sleep(5000)
        raise Exception(e)

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
            except Exception as e:
                subscriber.disconnect(self.__rely)
                self.__log.critical(f"Failed to connecting EDDN broker", exc_info=e)

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
            
            dataJson = simplejson.loads(dataDeCompress)
            if dataJson == False:
                self.__log.error(f"Failed to decode message")
            
            if dataJson['header']['softwareName'] in self.__authori_softwers:
                self.__log.debug(f"Received message from EDDN broker: {dataJson}")
                self.process(dataJson)

    def process(self, data:json):
        try:
            if data["$schemaRef"] == "https://eddn.edcd.io/schemas/journal/1":
                analytic = JournalAnalytic(data=data)
                analytic.analyst()
        except Exception as e:
            self.__log.critical(f"un errore da parte dei analisi dei dati: {e}")

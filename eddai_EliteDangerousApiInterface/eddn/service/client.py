from django.conf import settings
import zlib, zmq, json
from eddn.models import DataLog
from logging import getLogger
from eddn.service.dataAnalytics.utility import star_analytic

class EddnClient:
    """
    This class represents a client for the EDDN (Elite Dangerous Data Network) service.

    Attributes:
        __log (Logger): The logger instance for logging messages.
        __debug (bool): A flag indicating whether debug mode is enabled.
        __timeout (int): The timeout value for receiving messages from the EDDN broker.
        __rely (str): The address of the EDDN broker to connect to.
        __authori_softwers (list): A list of authorized software names.
        name (str): The name of the EDDN service.

    Methods:
        connect(): Connects to the EDDN broker and starts receiving messages.
        receive(subscriber: zmq.Socket): Receives messages from the EDDN broker and processes them.
    """
    __log = getLogger('eddn')
    __debug = settings.DEBUG
    __timeout = settings.EDDN_TIMEOUT
    __rely = settings.EDDN_RELY
    __authori_softwers = settings.AUTHORI_SED_SOFTWARS

    def connect(self):
        """
        Connects to the EDDN broker and starts receiving messages.

        Raises:
            zmq.ZMQError: If there is an error connecting to the EDDN broker.
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

    def receive(self, subscriber: zmq.Socket):
        """
        Receives messages from the EDDN broker and processes them.

        Args:
            subscriber (zmq.Socket): The subscriber socket for receiving messages.

        Raises:
            zlib.error: If there is an error decompressing the message.
            json.JSONDecodeError: If there is an error decoding the message.
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
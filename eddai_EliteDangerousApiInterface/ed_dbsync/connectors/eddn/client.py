import zlib, zmq, json
import logging

from django.conf import settings
from django.contrib.auth import authenticate

from ed_dbsync.tasks import AnalystTasck
from ed_dbsync.dataclass import IncomingData
from users.models import User

class EDDNClient:
    """
    This class represents a client for the EDDN (Elite Dangerous Data Network) service.

    Attributes:
        log (Logger): The logger instance for logging messages.
        debug (bool): A flag indicating whether debug mode is enabled.
        timeout (int): The timeout value for receiving messages from the EDDN broker.
        rely (str): The address of the EDDN broker to connect to.
        authori_softwers (list): A list of authorized software names.
        name (str): The name of the EDDN service.

    Methods:
        connect(): Connects to the EDDN broker and starts receiving messages.
        receive(subscriber: zmq.Socket): Receives messages from the EDDN broker and processes them.
    """
    log = logging.getLogger('eddn')
    timeout = settings.EDDN_TIMEOUT
    rely = settings.EDDN_RELY
    authori_softwers = settings.AUTHORI_SED_SOFTWARS

    _agent = None

    @property
    def agent(self) -> User:
        """
        restituisce l'utente utilizzato per inviare il datto
        """
        if not self._agent:
            self._agent = authenticate(
                username=settings.EDDN_USER_NAME_AGENT,
                password=settings.EDDN_USER_PASSWORD_AGENT
            )
        return self._agent

    def connect(self):
        """
        Connects to the EDDN broker and starts receiving messages.

        Raises:
            zmq.ZMQError: If there is an error connecting to the EDDN broker.
        """
        self.log.info("Create a Socket associated with this Context")
        context = zmq.Context()
        subscriber = context.socket(zmq.SUB)
        subscriber.setsockopt(zmq.SUBSCRIBE, b"")
        subscriber.setsockopt(zmq.RCVTIMEO, self.timeout)
        self.log.info("created a socket")
        while True:
            try:
                subscriber.connect(self.rely)
                self.log.info("Connecting to EDDN")
                self.receive(subscriber)
                self.log.error(f"Disconecter from {self.rely}")
            except zmq.ZMQError as e:
                subscriber.disconnect(self.rely)
                self.log.critical(f"Failed to connecting EDDN broker: %s", e, exc_info=True)

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
                self.log.error(f"The connection was lost From {self.rely}")
                break

            dataDeCompress = zlib.decompress(dataCompres)
            if dataDeCompress == False:
                self.log.error(f"Failed to decompress message")
                break
            
            dataJson = json.loads(dataDeCompress)
            if dataJson == False:
                self.log.error(f"Failed to decode message")
                break

            self.log.debug(f"Received and decompressed message: {dataJson}")

            if dataJson['header']['softwareName'] in self.authori_softwers:
                istance = IncomingData(data=dataJson, source="eddn")
                self.log.info(f"Send message to worker: {istance}", extra={'istance': istance})
                AnalystTasck().apply_async(
                    kwargs={'istance':istance, 'agent':self.agent}, 
                    queue="ed_dbsync"
                )
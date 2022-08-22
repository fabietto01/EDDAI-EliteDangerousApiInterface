from eddn.models import DataLog
from eddn.service.dataAnalytics.Erors import NotSerializerError
import logging
from rest_framework.serializers import Serializer

class BaseDataAnalytics(object):
    """
    classe base per l'analisi dei datti proveniente da eddn per poi dividerlo
    nei vari elaboratori
    """
    __log = logging.getLogger(__name__)

    def __init__(self, data:dict=None, instance:DataLog=None) -> None:
        self.instance = instance
        if self.instance is not None:
            data = self.instance.data
        self.data = data
                
    def get_message(self) -> dict:
        """
        ritorna il messagio all interno dei datti memorizzati nella classe
        """
        return self.data.get("message")

    def get_schema(self) -> str:
        """
        ritorna il nome dello schema dei dati
        """
        s = self.data.get("$schemaRef", None)
        s = s.replace("https://eddn.edcd.io/schemas/", "") if s else None
        return s.split("/")[0] if s else ""

    def get_analyst(self) -> Serializer:
        """
        funzione chiamata da analyst() per ottenere l'elaboratore dei datti piu coretto per
        il tipo di dati passati
        """
        raise NotImplementedError('`get_analyst()` must be implemented.')

    def analyst_error(self, str:str=None, analyst:Serializer=None):
        """
        chimma questa funzione quando qualcosa va storto cosi da salvare l'errore
        """
        if not self.instance is None:
            self.instance.error = {"error": f"{str}"} if str is not None else analyst.errors if analyst else {}
            self.instance.save(force_update=True)
        else:
            DataLog.objects.create(
                data=self.data,
                error={"error": f"{str}"} if str is not None else analyst.errors if analyst else {},
                schema=self.get_schema()
            )
        self.__log.error(f"analyst error -> {str if str else analyst.errors if analyst else 'unknown'}")
        
    def analyst(self):
        """
        chiama questa funzione per ottenere l'elaboratore dei datti
        """
        try:
            analyst = self.get_analyst()
            if analyst.is_valid():
                analyst.save()
            else:
                self.analyst_error(analyst=analyst)
        except NotSerializerError as e:
            self.analyst_error(str=e)
            return None
        except Exception as e:
            self.analyst_error(str=e)
            return None
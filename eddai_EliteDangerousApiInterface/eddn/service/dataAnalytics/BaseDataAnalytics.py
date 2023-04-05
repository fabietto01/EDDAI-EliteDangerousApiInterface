import logging
from eddn.models import DataLog
from eddn.service.dataAnalytics.Erors import NotSerializerError, NotDataContentError
from rest_framework.serializers import Serializer, ValidationError


class BaseDataAnalytics(object):

    __log = logging.getLogger("django")
    __regex = r"^https://eddn.edcd.io/schemas/(?P<schema>[a-z]{3,})/[1-9]"

    def __init__(self, istance:DataLog, *args, **kwargs):
        self.istance = istance
        if not self.istance.schema:
            import re
            s = re.search(self.__regex, self.istance.data.get("$schemaRef", None))
            self.istance.schema = s.group('schema')

    def get_message(self) -> dict:
        """
        ritorna il messagio all interno dei datti memorizzati nella classe
        """
        data = self.istance.data
        if not data:
            raise NotDataContentError("data not found")
        return data.get("message")
    
    def get_schema(self) -> str:
        return self.istance.schema

    def get_analyst(self) -> Serializer:
        """
        funzione chiamata da analyst() per ottenere l'elaboratore dei datti piu coretto per
        il tipo di dati passati
        """
        raise NotImplementedError('`get_analyst()` must be implemented.')
    
    def analyst(self):
        try:
            _analyst = self.get_analyst()
            _analyst.is_valid(raise_exception=True)
            _analyst.save()
            self.istance.error = None
        except ValidationError as e:
            self.__log.exception(f"error validating '{self.get_schema()}': %s", e)
            self.istance.error = _analyst.errors
            self.istance.save()
        except NotSerializerError as e:
            self.__log.debug(f"error in data analysis '{self.get_schema()}': %s", e)
            self.istance.error = {"error": f"{e}"}
            self.istance.save()
        except Exception as e:
            self.__log.exception(f"generic error in data analysis '{self.get_schema()}': %s", e)
            self.istance.error = {"error": f"{e}"}
            self.istance.save()
        return self.istance
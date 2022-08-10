from eddn.service.dataAnalytics.BaseDataAnalytics import BaseDataAnalytics
from eddn.service.dataAnalytics.Erors import NotSerializerError
from rest_framework.serializers import Serializer

class JournalAnalytic(BaseDataAnalytics):

    def get_event(self) -> str:
        """
        ritorna la stigra del evento
        """
        return self.get_message().get("event", '')


    def get_analyst(self) -> Serializer:
        """
        funzione chiamata da analyst() per ottenere l'elaboratore dei datti piu coretto per
        il tipo di dati passati
        """
        try:
            func = getattr(self, f"analyst_{self.get_event()}")
        except AttributeError as e:
            raise NotSerializerError(f"the service has not yet analyzed this event -> {e}")
        else:
            return func()

    def analyst_FSDJump(self):
        data = self.get_message()
        pass
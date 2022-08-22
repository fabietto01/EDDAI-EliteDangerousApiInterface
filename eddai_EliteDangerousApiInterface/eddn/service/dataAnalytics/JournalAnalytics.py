from eddn.service.dataAnalytics.BaseDataAnalytics import BaseDataAnalytics
from eddn.service.dataAnalytics.Erors import NotSerializerError
from rest_framework.serializers import Serializer

from eddn.service.journals.FSDJumpSerializer import FSDJumpSerializer

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
            raise NotSerializerError(f"the service has not yet analyzed this event '{self.get_event()}'")
        else:
            return func()

    def analyst_FSDJump(self):
        data = self.get_message()
        for attr, value in data.items():
            if attr in ('Powers', 'PowerplayState'):
                dwadadawd= 3
            elif attr == "Factions":
                for faction in value:
                    for attr2, value2 in faction.items():
                        if attr2 in ('HomeSystem', 'SquadronFaction'):
                            dwadadawd= 3
        if data.get('Factions', []) != []:
            dwadadawd= 3
        return FSDJumpSerializer(data=data)
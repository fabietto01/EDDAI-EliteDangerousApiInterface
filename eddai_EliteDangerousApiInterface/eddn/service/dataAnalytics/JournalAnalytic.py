from eddn.service.dataAnalytics.BaseDataAnalytics import BaseDataAnalytics
from eddn.service.dataAnalytics.Erors import NotSerializerError
from rest_framework.serializers import Serializer

from eddn.service.serializer.journals import (
    FSDJumpSerializer, StarScanSerializer, PlanetScanSerializer,
    SAASignalsFoundHotspotSerializers, SAASignalsFoundSignalAndSampleSerializers,
    DockedSerializer, LocationSerializer, CarrierJumpSerializer
)

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
        
    def analyst_Docked(self):
        data=self.get_message()
        return DockedSerializer(data=data)

    def analyst_FSDJump(self):
        data = self.get_message()
        for attr, value in data.items():
            if attr == "Factions":
                for faction in value:
                    for attr2, value2 in faction.items():
                        if attr2 in ('HomeSystem', 'SquadronFaction'):
                            dwadadawd= 3
            elif attr == "Conflicts":
                dadwad = 3
        return FSDJumpSerializer(data=data)

    def analyst_Scan(self):
        data = self.get_message()
        if not 'Ring' in data.get('BodyName', ''):
            if 'StarType' in data.keys():
                return StarScanSerializer(data=data)
            return PlanetScanSerializer(data=data)
        raise NotSerializerError(
            f"the service with this '{self.get_event()}' event, is not able to scan bodies that have inside the name 'Ring'"
        )

    def analyst_Location(self):
        data=self.get_message()
        return LocationSerializer(data=data)

    def analyst_SAASignalsFound(self):
        data=self.get_message()
        if 'Ring' in data.get('BodyName', ''):
            return SAASignalsFoundHotspotSerializers(data=data)
        return SAASignalsFoundSignalAndSampleSerializers(data=data)
    
    def analyst_CarrierJump(self):
        data=self.get_message()
        return CarrierJumpSerializer(data=data)
    
    def analyst_CodexEntry(self):
        data=self.get_message()
        raise NotSerializerError(
            f"the service with this '{self.get_event()}' event, is not able to analyze this event"
        )
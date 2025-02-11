from .baseDataAnalysis import BaseDataAnalysis
from .errors import NotSerializerError

from ..serializers.journal import DockedSerializer, FSDJumpSerializer, BaseScanSerializer, PlanetScanSerializer

class JournalAnalysis(BaseDataAnalysis):

    def get_event(self) -> str:
        mesaage = self.get_message()
        return mesaage.get("event")

    def get_serializer_class(self):
        try:
            func = getattr(self, f"serializer_{self.get_event()}")
        except AttributeError as e:
            raise NotSerializerError(f"the service has not yet analyzed this event '{self.get_event()}'")
        else:
            return func()

    # def serializer_FSDJump(self):
    #     return FSDJumpSerializer
    
    # def serializer_Docked(self):
    #     return DockedSerializer
    
    def serializer_Scan(self):
        message = self.get_message()
        if not 'Ring' in message.get('BodyName', ''):
            if 'StarType' in message.keys():
                return BaseScanSerializer
            return PlanetScanSerializer
        raise NotSerializerError(
            f"the service with this '{self.get_event()}' event, is not able to scan bodies that have inside the name 'Ring'"
        )
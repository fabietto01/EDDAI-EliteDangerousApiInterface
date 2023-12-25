from celery.result import AsyncResult

from ..celey.Task import DSTasck as Task
from ..models import Service as ServiceModel, ServiceEvent

class CheckService(Task):

    name = "djnago_service.backend.CheckService"

    def run(self, worker:str, *args, **kwargs):
        
        self.log.info("CheckService Start")
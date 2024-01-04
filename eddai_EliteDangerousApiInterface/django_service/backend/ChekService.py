from celery import Celery
from celery.result import AsyncResult
from celery.app.control import Control, Inspect

import re
import uuid

from ..celery.Service.BeseService import BeseService
from ..models import Service as ServiceModel, ServiceEvent
from ..conf import servis_settings

class CheckService(BeseService):

    name = "djnago_service.backend.CheckService"
    
    in_check_update = [
        ServiceModel.StatusChoices.STARTING.value,
        ServiceModel.StatusChoices.RUN.value,
        ServiceModel.StatusChoices.STOPING.value,
        ServiceModel.StatusChoices.STOP.value,
    ]

    def run(self, *args, **kwargs):
        self.log.info("CheckService Start")

        control:Control = self.app.control

        workers = self._get_worker_list(control)

        inspect:Inspect = control.inspect(workers)

        querry = ServiceModel.objects.filter(status__in=self.in_check_update)

        for service_model in querry:
            update = False

            worker, service = self._get_service(service_model.id, inspect)

            try:
                if self._update_to_stop(service, service_model):
                    service_model.status = ServiceModel.StatusChoices.STOP.value
                    update = True
                elif self._update_to_run(service, service_model):
                    service_model.status = ServiceModel.StatusChoices.RUN.value
                    update = True
            except Exception as e:
                self.log.error(
                    f"Error in update {service_model.name}",
                    exc_info=e
                )
            else:
                if update:
                    service_model.save()

    def _get_service(self, serialized_id:uuid, inspect:Inspect) -> tuple[str, dict]:
        service:dict = {}
        worker:str = None
        service_dict = inspect.query_task(serialized_id)
        for kay, value in service_dict.items():
            if not value in (None, {}):
                service = value
                worker = kay
        return worker, service

    def _get_worker_list(self, control:Control) -> list[str]:
        """
        Get list of worker name
        """
        workers = []
        for worker in control.ping():
            worker_name = list(worker.keys())[0]
            if re.match(servis_settings.SERVICE_WORKER_NAME, worker_name):
                workers.append(worker_name)
        return workers
    
    def _update_to_stop(self, service:dict, service_model:ServiceModel) -> bool:
        """
        Check is service stop
        """
        if service_model.status == ServiceModel.StatusChoices.STOP.value:
            return False
        if service in (None, {}):
            return True
        return False
    
    def _update_to_run(self, service:dict, service_model:ServiceModel) -> bool:
        """
        Check is service start
        """
        if service_model.status == ServiceModel.StatusChoices.RUN.value:
            return False
        if not service in (None, {}):
            id = str(service_model.id)
            result = AsyncResult(id)
            state = result.status
            return state == ServiceModel.StatusChoices.RUN.label
        return False
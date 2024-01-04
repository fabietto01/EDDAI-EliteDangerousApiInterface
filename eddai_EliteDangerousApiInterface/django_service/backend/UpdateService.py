from celery.result import AsyncResult

from ..celery.Service.BeseService import BeseService
from ..celery.utility import memcache_lock
from ..models import Service as ServiceModel, ServiceEvent

class UpdateService(BeseService):

    name = "djnago_service.backend.UpdateService"

    def run(self, serialized_id:int, *args, **kwargs):

        lock_id = f"{self.name}_{serialized_id}"

        with memcache_lock(lock_id, self.app.oid, 60 * 10) as acquired:
            if acquired:
                service = self._get_service(serialized_id)

                self.log.info(
                    f"UpdateService Start for {service.name}"
                )

                event, create = self.get_event(service)
                
                if create:
                    self.log.debug(
                        f"A new event has been created for {service.name}"
                    )
                    return
                
                if event.event != service.status:

                    self.log.debug(
                        f"Update detected {service.name}"
                    )

                    self.create_event(service, **kwargs)

                    if service.status == ServiceModel.StatusChoices.STARTING:
                        async_result = self.start_service(service)
                    elif service.status == ServiceModel.StatusChoices.STOPING:
                        async_result = self.stop_service(service)
                    else:
                        self.log.debug(
                            f"Not Action for {service.name}"
                        )
                else:
                    self.log.debug(
                        f"No Update detected for {service.name}"
                    )

                self.log.info(
                    f"is UpdateService End for {service.name}"
                )

    def get_event(self, service:ServiceModel) -> tuple[ServiceEvent, bool]:
        """
        Get last event or create new
        """
        created = False
        event = ServiceEvent.objects.filter(service=service).order_by("-created").first() or None
        if event is None:
            event = self.create_event(service)
            created = True
        return event, created
    
    def create_event(self, service:ServiceModel, meta:str=None) -> ServiceEvent:
        """
        Create new event
        """
        return ServiceEvent.objects.create(
            service=service,
            event=service.status,
            meta=meta
        )

    def start_service(self, service:ServiceModel) -> AsyncResult:
        """
        start service
        """
        self.log.debug(
            f"Start Service {service.name}"
        )
        return self.app.send_task(
            task_id=str(service.id),
            name=service.service,
            args=service.args,
            kwargs=service.kwargs,
            routing_key=service.routing_key
        )
    
    def stop_service(self, service:ServiceModel) -> AsyncResult:
        """
        stop service
        """
        self.log.debug(
            f"Stop Service {service.name}"
        )
        return self.app.control.revoke(
            task_id=str(service.id),
            terminate=True
        )
    
    def on_failure(self, exc, task_id, args, kwargs, einfo,):
        """	
        nel caso in cui il servizio fallisce, segla il servizio come errore
        """
        serialized_id = kwargs.get("serialized_id", None)
        if serialized_id:
            service = self._get_service(serialized_id)
            service.status = ServiceModel.StatusChoices.ERROR.value
            service.save()
            self.create_event(service, exc)
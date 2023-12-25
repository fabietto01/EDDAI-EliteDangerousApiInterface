from .BeseService import BeseService
from ..Request import ServiceRequest

from ...models import Service as ServiceModel

class Service(BeseService):

    #https://docs.celeryq.dev/en/stable/userguide/tasks.html#retrying
    autoretry_for = (Exception,)
    max_retries = None
    retry_backoff = 5
    retry_backoff_max = 30
    retry_jitter = True
    track_started = True
    #https://docs.celeryq.dev/en/stable/userguide/tasks.html#requests-and-custom-requests
    Request = ServiceRequest

    def update_state(self, task_id=None, state:ServiceModel.StatusChoices=None, meta=None, **kwargs):
        """
        aggiorna lo statto del servizio sia nel modello che nel task
        """

        if type(state) is type(ServiceModel.StatusChoices):

            if task_id is None:
                task_id = self.request.id
            
            service = self._get_service(task_id)
            service.status = state.value
            service.set_meta_status = meta
            service.save()

        return super().update_state(task_id, state.label, meta, **kwargs)

    def before_start(self, task_id, args, kwargs):
        self.update_state(state=ServiceModel.StatusChoices.RUN)
    
    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        self.update_state(state=ServiceModel.StatusChoices.STOP)
    
    def on_retry(self, *args, **kwargs):
        _str = f"Retry in max {self.retry_backoff_max} seconds..."
        self.update_state(
            state=ServiceModel.StatusChoices.RETRY,
            meta={"retry": _str}
        )
        self.log.info(_str)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        _str = f"Service {self.name} failed: {exc}"
        self.update_state(
            state=ServiceModel.StatusChoices.CRASH,
            meta={"exc": _str}
        )
        self.log.critical("Service failed" , exc_info=True)
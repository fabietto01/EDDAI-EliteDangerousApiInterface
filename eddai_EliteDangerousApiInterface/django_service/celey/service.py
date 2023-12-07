from celery import Task
from celery.utils.log import get_task_logger

from ..models import ServiceEvent

from .request import ServiceRequest

class Service(Task):

    log  = get_task_logger(__name__)
    name = f"{__name__}"
    #https://docs.celeryq.dev/en/stable/userguide/tasks.html#retrying
    autoretry_for = (Exception,)
    max_retries = None
    retry_backoff = 5
    retry_backoff_max = 30
    retry_jitter = True
    track_started = True
    #https://docs.celeryq.dev/en/stable/userguide/tasks.html#requests-and-custom-requests
    Request = ServiceRequest

    def before_start(self, task_id, args, kwargs):
        self.update_state(state=ServiceEvent.EventChoices.RUN.label)
        return super().before_start(task_id, args, kwargs)

    def run(self, *args, **kwargs):
        return super().run(*args, **kwargs)
    
    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        self.update_state(state=ServiceEvent.EventChoices.STOP.label)
        return super().after_return(status, retval, task_id, args, kwargs, einfo)
    
    def on_retry(self, *args, **kwargs):
        _str = f"Retry in max {self.retry_backoff_max} seconds..."
        self.update_state(
            state=ServiceEvent.EventChoices.ERROR.label,
            meta={"text": _str}
        )
        self.log.info(_str)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        _str = f"Service {self.name} failed: {exc}"
        self.update_state(
            state=ServiceEvent.EventChoices.CRASH.label,
            meta={"text": _str}
        )
        self.log.critical("Service failed" , exc_info=True) #exc_info=True
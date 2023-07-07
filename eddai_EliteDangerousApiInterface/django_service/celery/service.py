from celery import Task
from celery.utils.log import get_task_logger

class BaseService(Task):

    log  = get_task_logger(__name__)
    name = f"Service{__name__}"
    #https://docs.celeryq.dev/en/stable/userguide/tasks.html#retrying
    autoretry_for = (Exception,)
    max_retries = None
    retry_backoff = 5
    retry_backoff_max = 30
    retry_jitter = True
    track_started = True

    def run(self, *args, **kwargs):
        return super().run(*args, **kwargs)
    
    def on_retry(self, *args, **kwargs):
        self.log.info(f"Retry in max {self.retry_backoff_max} seconds...")

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        self.log.critical(f"Failed to EDDN: %s", exc , exc_info=True) #exc_info=True

    
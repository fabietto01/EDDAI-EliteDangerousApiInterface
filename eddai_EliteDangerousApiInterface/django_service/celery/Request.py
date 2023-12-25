from celery.worker.request import Request
from celery.utils.log import get_task_logger

class ServiceRequest(Request):
    """
    
    """
    log = get_task_logger(__name__)

    def on_timeout(self, soft, timeout):
        return super().on_timeout(soft, timeout)
    
    def on_failure(self, exc_info, send_failed_event=True, return_ok=False):
        return super().on_failure(exc_info, send_failed_event, return_ok)
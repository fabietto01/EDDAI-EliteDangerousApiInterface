from celery.worker.request import Request
from celery.utils.log import get_task_logger

class ServiceRequest(Request):
    """
    
    """
    log = get_task_logger(__name__)
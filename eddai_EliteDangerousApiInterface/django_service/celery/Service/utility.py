from celery import shared_task
from celery import Celery
from .Service import Service

from django.conf import settings

def shared_service(base=Service, *args, **kwargs):
    """
    Decorator to create a shared task class out of any class-based task.
    """
    return shared_task(base=base,*args, **kwargs)

def get_servis_list(app:Celery) -> list[Service]:
    service = []
    for task_name, task_obj in app.tasks.items():
        if issubclass(task_obj.__class__, Service) or settings.DEBUG:
            service.append(task_name)
    return service
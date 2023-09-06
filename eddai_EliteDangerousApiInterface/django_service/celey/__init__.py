from celery import shared_task
from .service import Service

def shared_service(base=Service, *args, **kwargs):
    return shared_task(base=base,*args, **kwargs)
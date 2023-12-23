from celery import shared_task
from .service import Service
from .utility import *

def shared_service(base=Service, *args, **kwargs):
    return shared_task(base=base,*args, **kwargs)
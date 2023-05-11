from celery import shared_task

from eddn.service.client import EddnClient

@shared_task(retry=False)
def eddn():
    cl = EddnClient()
    cl.start()
from celery.signals import worker_ready
from celery.worker.consumer import Consumer
from eddn.tasks import EddnClient

@worker_ready.connect
def at_start(sender:Consumer, **kwargs):
    if sender and str(sender.hostname).startswith('workerEDDN'):
        EddnClient.apply_async(routing_key=sender.hostname, priority=9)
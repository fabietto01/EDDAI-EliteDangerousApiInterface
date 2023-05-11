from celery.signals import worker_ready
from celery.worker.consumer import Consumer
from eddn.service.client import EddnClient

@worker_ready.connect
def at_start(sender:Consumer, **kwargs):
    if str(sender.hostname).startswith('workerEDDN'):
        with sender.app.connection() as conn:
            sender.app.send_task("eddn.tasks.eddn", connection=conn)
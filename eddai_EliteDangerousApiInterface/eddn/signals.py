from celery.signals import worker_ready
from celery.worker.consumer import Consumer
from eddn.tasks import EddnClient

@worker_ready.connect
def at_start(sender:Consumer, **kwargs):
    if sender and str(sender.hostname).startswith('workerEDDN'):
        with sender.app.connection() as conn:
            sender.app.send_task('ServiceEDDN', connection=conn,)
            EddnClient.apply_async(connection=conn, priority=9)
from celery.signals import worker_ready
from eddn.service.client import EddnClient

@worker_ready.connect
def at_start(sender, **kwargs):
    if "workerEDDN" in sender:
        with sender.app.connection() as conn:
            sender.app.send_task("eddn.tasks.eddn", connection=conn)
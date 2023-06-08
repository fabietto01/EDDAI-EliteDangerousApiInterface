from celery.signals import worker_ready
from celery.worker.consumer import Consumer
from celery.app.control import Inspect
from typing import Any, Tuple

from eddn.tasks import EddnClient

@worker_ready.connect
def at_start(sender:Consumer, **kwargs):

    def tasck_is_running(inspector:Inspect,  task_name:str) -> Tuple[bool, str]:
        x = inspector.active()
        for worker in x:
            for task in worker:
                if task['name'] == task_name:
                    return True, task['id']
        return False, ''

    if sender and str(sender.hostname).startswith('workerEDDN'):
        with sender.app.connection() as conn:
            inspector:Inspect = sender.app.control.inspect()
            is_running, task_id = tasck_is_running(inspector, EddnClient.name)
            if is_running:
                sender.app.control.revoke(task_id, terminate=True)
            EddnClient().apply_async(
                connection=conn, priority=9,
            )
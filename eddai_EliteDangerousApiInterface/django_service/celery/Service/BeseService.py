from celery import Task
from celery._state import _task_stack
from celery.utils.log import get_task_logger
from logging import Logger
import uuid
from ...models import Service as ServiceModel

class BeseService(Task):
    
    log:Logger  = get_task_logger('Service')
    name = f"{__name__}"
    autoretry_for = ()
    max_retries = 0

    def _get_service(self, serialized_id:uuid) -> ServiceModel:
        return ServiceModel.objects.get(pk=serialized_id)

    def __call__(self, *args, **kwargs):
        _task_stack.push(self)
        self.push_request(args=args, kwargs=kwargs)
        try:
            return self.run(*args, **kwargs)
        finally:
            self.pop_request()
            _task_stack.pop()

    def run(self, *args, **kwargs):
        """The body of the task executed by workers."""
        raise NotImplementedError('Tasks must define the run method.')
from celery import Task
from celery.utils.log import get_task_logger
from logging import Logger
from ..models import Service as ServiceModel

class DSTasck(Task):
    
    log:Logger  = get_task_logger('Service')
    name = f"{__name__}"
    autoretry_for = ()
    max_retries = 0

    def _get_service(self, serialized_id) -> ServiceModel:
        return ServiceModel.objects.get(pk=serialized_id)

    def run(self, *args, **kwargs):
        """The body of the task executed by workers."""
        raise NotImplementedError('Tasks must define the run method.')
from celery import shared_task
from django_service.celey.cache import service_lock
from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_task(bind=True)
def add_eddn(self, x, y):

    lock_id = '{0}-lock-{1}-{2}'.format(self.name, x, y)

    logger.debug('inizio tasck: %s', lock_id)
    with service_lock(lock_id, self.app.oid) as acquired:
        if acquired:
            return x + y
    logger.debug('il %s e gia stato lavorato da un altro lavorato', lock_id)
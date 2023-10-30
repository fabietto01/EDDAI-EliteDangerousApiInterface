from .celey import shared_service
import time
import random

from eddai_EliteDangerousApiInterface.celery import app as celery_app
from celery.utils.log import get_task_logger
from django_service.celey.service import Service


logger = get_task_logger(__name__)

@shared_service(bind=True)
def test_service(self):
    
    x = 1

    while True:
        logger.info("questo è la ripetizione %s, del tentativo %s ", x, self.request.retries)
        if 1 == random.randint(1, 10):
           logger.info("lancio un eccezione")
           raise Exception("test")
        x += 1
        time.sleep(1)

class _TestService(Service):

    def run(self, *args, **kwargs):
        x = 1

        while True:
            logger.info("questo è la ripetizione %s, del tentativo %s ", x, self.request.retries)
            if 1 == random.randint(1, 10):
                self.log.info("lancio un eccezione")
                raise Exception("test")
            x += 1
            time.sleep(1)

celery_app.register_task(_TestService)
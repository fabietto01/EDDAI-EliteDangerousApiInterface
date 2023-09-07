from .celey import shared_service
import time
import random

from celery.utils.log import get_task_logger

logger = get_task_logger(__name__)

@shared_service(bind=True)
def test_service(self):
    
    x = 1

    while True:
        logger.info("questo è la ripetizione %s, del tentativo %s ", x, self.request.retries)
        #if 1 == random.randint(1, 10):
        #    logger.info("lancio un eccezione")
        #    raise Exception("test")
        x += 1
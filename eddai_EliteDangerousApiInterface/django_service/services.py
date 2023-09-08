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
        if 1 == random.randint(1, 10):
           logger.info("lancio un eccezione")
           raise Exception("test")
        x += 1
        time.sleep(1)


        #c5f84630-6dd9-492d-8b33-c08b3bd17bb6
        #c5f84630-6dd9-492d-8b33-c08b3bd17bb6
        #7e51aadb-9324-4502-9154-eb30c8529737
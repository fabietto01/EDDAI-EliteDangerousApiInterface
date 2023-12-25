from .celey import shared_service
import time
import random

from eddai_EliteDangerousApiInterface.celery import app as celery_app
from celery.utils.log import get_task_logger
from django_service.celey import Service


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

    name = "django_service.services._TestService"

    def run(self, max_retries:int, max_random:int, *args, **kwargs):
        
        ciclo = True
        ciclo_namber = 1

        while ciclo:
            self.log.info(
                f"Questo é il ciclo {ciclo_namber}, del tentativo {self.request.retries}, di {max_retries}"
            )
            if self.request.retries >= max_retries:
                ciclo = False
            elif 1 == random.randint(1, max_random):
                self.log.info("lancio un eccezione")
                raise Exception("test")
            ciclo_namber += 1
            time.sleep(1)
        self.log.info("ciclo finito")

celery_app.register_task(_TestService)
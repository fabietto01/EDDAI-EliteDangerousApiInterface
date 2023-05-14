from eddai_EliteDangerousApiInterface.celery import app as celery_app
from eddn.service.client import EddnClient
from eddn.tasks.tasks import *

celery_app.register_task(EddnClient)

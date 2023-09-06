from eddai_EliteDangerousApiInterface.celery import app as celery_app
from .client import EddnClient

celery_app.register_task(EddnClient)
from eddai_EliteDangerousApiInterface.celery import app
from .analyst import AnalystTasck

app.register_task(AnalystTasck())
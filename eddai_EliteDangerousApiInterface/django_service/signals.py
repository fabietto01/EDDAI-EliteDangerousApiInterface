from celery.app import app_or_default
from celery import Celery

app:Celery = app_or_default



@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    x =1

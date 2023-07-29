from django_service import app
from celery import Celery

@app.on_after_configure.connect
def setup_periodic_tasks(sender:Celery, **kwargs):
    typeRoutes = type(app.conf.task_routes)
    defaiult = app.conf.task_routes

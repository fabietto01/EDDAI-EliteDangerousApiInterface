from celery import Celery
from celery.app.control import Control, Inspect
from celery import _state
from .service import Service

def get_app() -> Celery:
    x = _state.get_current_app()
    return x

def get_control(app:Celery) -> Control:
    return app.control

def get_inspect(app:Celery) -> Inspect:
    control = get_control(app)
    return control.inspect()

def get_servis_list(app:Celery) -> list[Service]:
    service = []
    app.tasks
    for task_name, task_obj in app.tasks.items():
        if issubclass(task_obj.__class__, Service):
            service.append(task_name)
    return service
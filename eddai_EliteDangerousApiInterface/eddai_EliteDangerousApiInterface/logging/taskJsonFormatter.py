from pythonjsonlogger.jsonlogger import JsonFormatter
from celery._state import get_current_task


class TaskJsonFormatter(JsonFormatter):

    def format(self, record):
        """"
        Codice preso da celery.app.log.TaskFormatter per recuperare gli id del task
        """
        task = get_current_task()
        if task and task.request:
            record.__dict__.update(task_id=task.request.id,
                                   task_name=task.name)
        else:
            record.__dict__.setdefault('task_name', '???')
            record.__dict__.setdefault('task_id', '???')
        return super().format(record)
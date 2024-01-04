from celery.signals import celeryd_init
from celery import Celery

import re
import logging

from ..celery import app
from ..conf import servis_settings

logger = logging.getLogger("django")

@celeryd_init.connect
def setap_config(sender, conf, *args, **kwargs):
    """
    Set default queue for service
    """
    if re.match(servis_settings.SERVICE_WORKER_NAME, sender):
        conf.task_default_queue = servis_settings.SERVICE_DEFAULT_QUEUE

@app.on_after_finalize.connect
def setup_periodic_tasks(sender:Celery, **kwargs):
    """
    Setup periodic tasks
    """
    from .ChekService import CheckService

    logger.info("Setup periodic tasks")
    try:
        sender.add_periodic_task(
            30.0,
            CheckService().s(),
            name="CheckService-30s",
            queue=servis_settings.SERVICE_DEFAULT_QUEUE
        )
    except Exception as e:
        logger.error(
            "Error setup periodic tasks",
            exc_info=e
        )
    logger.info("Complit Setup periodic tasks")
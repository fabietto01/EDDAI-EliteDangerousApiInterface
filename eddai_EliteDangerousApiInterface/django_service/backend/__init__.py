from celery.signals import celeryd_init

from django.db.models.signals import post_save
from django.dispatch import receiver

import re

from ..conf import servis_settings
from ..models import Service
from ..celey.utility import get_app

from .UpdateService import UpdateService

app = get_app()
app.register_task(UpdateService())

@celeryd_init.connect
def setap_config(sender, conf, *args, **kwargs):
    """
    Set default queue for service
    """
    if re.match(servis_settings.SERVICE_WORKER_NAME, sender):
        conf.task_default_queue = servis_settings.SERVICE_DEFAULT_QUEUE

@receiver(post_save, sender=Service)
def update_service(sender, instance:Service, **kwargs):
    kwargs={'serialized_id': instance.pk}
    if instance.get_meta_status:
        kwargs.update({'meta': instance.get_meta_status})
    UpdateService().apply_async(
        kwargs=kwargs,
        queue=servis_settings.SERVICE_DEFAULT_QUEUE
    )
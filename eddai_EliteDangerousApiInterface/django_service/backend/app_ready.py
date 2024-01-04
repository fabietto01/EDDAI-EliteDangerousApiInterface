from django.db.models.signals import post_save
from django.dispatch import receiver

from ..models import Service

from ..celery import app
from ..conf import servis_settings

from .UpdateService import UpdateService
from .ChekService import CheckService

app.register_task(UpdateService())
app.register_task(CheckService())

@receiver(post_save, sender=Service)
def update_service(sender, instance:Service, **kwargs):
    kwargs={'serialized_id': instance.pk}
    if instance.get_meta_status:
        kwargs.update({'meta': instance.get_meta_status})
    UpdateService().apply_async(
        kwargs=kwargs,
        queue=servis_settings.SERVICE_DEFAULT_QUEUE
    )
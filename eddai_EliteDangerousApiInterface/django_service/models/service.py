from collections.abc import Iterable
from django.db import models
from django.utils.translation import gettext_lazy as _

from ..conf import servis_settings

import uuid

# Create your models here.

class Service(models.Model):
    
    class StatusChoices(models.IntegerChoices):
        STARTING = 5, _("STARTING...")
        RUN = 10, _("RUN")
        STOPING = 15, _("STOPING...")
        STOP = 20, _("STOP")
        ERROR = 25, _("ERROR")
        CRASH = 30, _("CRASH")

    def _args_default (): return []

    def _kwargs_default (): return {}

    def _routing_key_default (): return servis_settings.SERVICE_DEFAULT_QUEUE

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(
        max_length=200, unique=True,
        verbose_name=_('Name'),
        help_text=_('Short Description For This Task'),
    )
    service = models.CharField(
        max_length=200, unique=True,
        verbose_name=_('Service Name'),
        help_text=_('The Name of the Service that Should be Run.  '
                    '(Example: "proj.tasks.import_contacts")'),
    )
    status = models.PositiveSmallIntegerField(
        choices=StatusChoices.choices,
        default=StatusChoices.STOP,
    )
    _meta_status = None
    args = models.JSONField(
        blank=True, default=_args_default,
        verbose_name=_('Positional Arguments'),
        help_text=_(
            'JSON encoded positional arguments '
            '(Example: ["arg1", "arg2"])'),
    )
    kwargs = models.JSONField(
        blank=True, default=_kwargs_default,
        verbose_name=_('Keyword Arguments'),
        help_text=_(
            'JSON encoded keyword arguments '
            '(Example: {"argument": "value"})'),
    )
    routing_key = models.CharField(
        max_length=200, blank=True, null=True, 
        default=_routing_key_default,
        verbose_name=_('Routing Key'),
        help_text=_('Override Routing Key for low-level AMQP routing'),
    )

    def __str__(self):
        return self.name
    
    @property
    def get_meta_status(self):
        return self._meta_status
    
    @get_meta_status.setter
    def set_meta_status(self, value:str=None):
        if value:
            self._meta_status = str(value)
    
    class Meta:
        verbose_name = _("service")
        verbose_name_plural = _("services")
        ordering  = ["name"]
        indexes = [
            models.Index(fields=["status"], name="status_index"),
            models.Index(fields=["routing_key"], name="routing_key_index")
        ]
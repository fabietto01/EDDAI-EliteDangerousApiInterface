from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Service(models.Model):
    
    class StatusChoices(models.TextChoices):
        RUN = 'r', _("RUN")
        STOP = 's', _("STOP") 
        ERROR = 'e', _("ERROR")
        
        __empty__ = _("(Unknown)")

    name = models.CharField(
        max_length=200, unique=True,
        verbose_name=_('Name'),
        help_text=_('Short Description For This Task'),
    )
    task = models.CharField(
        max_length=200, unique=True,
        verbose_name=_('Task Name'),
        help_text=_('The Name of the Celery Task that Should be Run.  '
                    '(Example: "proj.tasks.import_contacts")'),
    )
    status = models.CharField(
        max_length=1,
        choices=StatusChoices.choices
    )
    args = models.TextField(
        blank=True, default='[]',
        verbose_name=_('Positional Arguments'),
        help_text=_(
            'JSON encoded positional arguments '
            '(Example: ["arg1", "arg2"])'),
    )
    kwargs = models.TextField(
        blank=True, default='{}',
        verbose_name=_('Keyword Arguments'),
        help_text=_(
            'JSON encoded keyword arguments '
            '(Example: {"argument": "value"})'),
    )
    routing_key = models.CharField(
        max_length=200, blank=True, null=True, default=None,
        verbose_name=_('Routing Key'),
        help_text=_('Override Routing Key for low-level AMQP routing'),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("service")
        verbose_name_plural = _("services")
        ordering  = ["name"]
        indexes = [
            models.Index(fields=["status"], name="status_index"),
            models.Index(fields=["routing_key"], name="routing_key_index")
        ]
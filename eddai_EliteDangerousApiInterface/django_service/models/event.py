from django.db import models
from django.utils.translation import gettext_lazy as _

from .service import Service

class ServiceEvent(models.Model):

    class EventChoices(models.TextChoices):
        START = 's', _("START")
        STOP = 's', _("STOP") 
        TRY = 't', _("TRY")
        ERROR = 'e', _("ERROR")

    service = models.ForeignKey(
        Service, on_delete=models.CASCADE,
        verbose_name=_("service"),
        related_name="events",
        related_query_name="event"
    )
    created = models.DateTimeField(
        verbose_name=_("created"),
        auto_now_add=True
    )

    class Meta:
        verbose_name = _("event")
        verbose_name_plural = _("events")
        ordering  = ["created"]
        indexes = [
            models.Index(fields=["service"], name="service_id_index")
        ]
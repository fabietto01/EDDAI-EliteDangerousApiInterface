from django.db import models
from django.utils.translation import gettext_lazy as _

from .Service import Service

class ServiceEvent(models.Model):

    service = models.ForeignKey(
        Service, on_delete=models.CASCADE,
        verbose_name=_("service"),
        related_name="events",
        related_query_name="event"
    )
    event = models.PositiveSmallIntegerField(
        verbose_name=_("event"),
        choices=Service.StatusChoices.choices,
    )
    created = models.DateTimeField(
        verbose_name=_("created"),
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.service} - { Service.StatusChoices(self.event).label}"

    class Meta:
        verbose_name = _("event")
        verbose_name_plural = _("events")
        ordering  = ["-created"]
        indexes = [
            models.Index(fields=["service"], name="service_id_index"),
            models.Index(fields=["event"], name="event_index")
        ]
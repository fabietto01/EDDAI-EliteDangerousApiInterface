from django.db import models
from django.utils.translation import gettext_lazy as _

class ServiceEvent(models.Model):

    class EventChoices(models.TextChoices):
        START = 'st', _("START")
        RUN = 'r', _("RUN")
        STOP = 'sp', _("STOP")
        ERROR = 'e', _("ERROR")
        CRASH = 'c', _("CRASH")

    service = models.ForeignKey(
        "django_service.Service", on_delete=models.CASCADE,
        verbose_name=_("service"),
        related_name="events",
        related_query_name="event"
    )
    event = models.CharField(
        verbose_name=_("event"),
        max_length=2,
        choices=EventChoices.choices,
    )
    created = models.DateTimeField(
        verbose_name=_("created"),
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.service} - { ServiceEvent.EventChoices(self.event).label}"

    class Meta:
        verbose_name = _("event")
        verbose_name_plural = _("events")
        ordering  = ["-created"]
        indexes = [
            models.Index(fields=["service"], name="service_id_index"),
            models.Index(fields=["event"], name="event_index")
        ]
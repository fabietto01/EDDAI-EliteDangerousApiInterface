from django.db import models
from django.utils.translation import gettext_lazy as _


class ServiceInStation(models.Model):
    station = models.ForeignKey(
        'ed_station.Station', on_delete=models.CASCADE,
        verbose_name=_('station'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )
    service = models.ForeignKey(
        'ed_station.Service', on_delete=models.CASCADE,
        verbose_name=_('service'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )
    updated = models.DateTimeField(
        auto_now=True
    )
    created = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        verbose_name = _('service in station')
        verbose_name_plural = _('services in station')
        indexes = [
            models.Index(fields=['station'], name='station_idx'),
            models.Index(fields=['service'], name='service_idx'),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['station', 'service'], name='unique_service_in_station'
            )
        ]
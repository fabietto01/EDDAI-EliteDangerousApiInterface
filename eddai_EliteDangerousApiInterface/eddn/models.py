from django.db import models

from django.utils.translation import gettext_lazy as _

# Create your models here.


class DataLog(models.Model):
    data = models.JSONField(
        verbose_name=_('data')
    )
    schema = models.CharField(
        verbose_name=_("schema"), max_length=100,
    )
    error = models.JSONField(
        verbose_name=_('error'), null=True, blank=True
    )
    update = models.DateTimeField(
        verbose_name=_("update"), auto_now=True,
    )

    class Meta:
        verbose_name = _("data log")
        verbose_name_plural = _("data logs")
        ordering = ['-update']


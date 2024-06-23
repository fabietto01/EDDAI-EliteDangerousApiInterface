from django.db import models
from django.contrib import admin

from django.utils.translation import gettext_lazy as _
from eddn.manager import EddnManager

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
    creat_at = models.DateTimeField(
        verbose_name=_("create at"), auto_now_add=True,
    )

    def __str__(self) -> str:
        return str(self.schema)

    class Meta:
        verbose_name = _("data log")
        verbose_name_plural = _("data logs")
        ordering = ['-update']

class AbstractDataEDDN(models.Model):
    """
    modelo astrato utilizato per unificare il salvatagio e la lettura dei dati
    che vengo utilizati per verificare e mapare i datti di eddn
    """
    name = models.CharField(
        max_length=255, verbose_name=_('name')
    )
    _eddn = models.CharField(
        max_length=100, unique=True, 
        blank=True, null=True
    )

    objects = EddnManager()

    @property
    @admin.display(ordering="_eddn", description="value for eddn")
    def eddn(self) -> str:
        if self.__eddn:
            return self.__eddn
        return self.name

    @eddn.setter
    def eddn(self, value: str) -> None:
        self.__eddn = value

    class Meta:
        abstract = True
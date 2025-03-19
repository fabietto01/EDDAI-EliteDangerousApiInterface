from django.db import models
from core.models import DateModels
from django.core.exceptions import ValidationError
from django.db.models.functions import Coalesce
from django.contrib import admin

from django.utils.translation import gettext_lazy as _

from .manager import EddnManager

class DataLog(DateModels):

    data = models.JSONField(
        verbose_name=_('data')
    )
    error = models.JSONField(
        verbose_name=_('error'), null=True, blank=True
    )
    _count = models.PositiveSmallIntegerField(
        verbose_name=_('count'), default=0
    )
    
    @property
    @admin.display(description=_('schema'))
    def schema(self) -> str:
        return self.data.get("$schemaRef", None)
    
    @property
    @admin.display(description=_('message'))
    def message(self) -> dict:
        return self.data.get("message", None)
    
    def __str__(self) -> str:
        return str(self.pk) or str(self.schema)
    
    def save(self, *args, **kwargs):
        if self.pk:
            self._count = self._count + 1
        return super().save(*args, **kwargs)

    class Meta:
        verbose_name = _("data log")
        verbose_name_plural = _("data logs")
        ordering = ['-updated_at']

class AbstractDataEDDN(models.Model):
    """
    modelo astrato utilizato per unificare il salvatagio e la lettura dei dati
    che vengo utilizati per verificare e mapare i datti di eddn
    """
    name = models.CharField(
        max_length=255, verbose_name=_('name'),
        unique=True,
    )
    _eddn = models.CharField(
        max_length=100, 
        blank=True, null=True,
    )
    eddn = models.GeneratedField(
        verbose_name=_('eddn'),
        expression=Coalesce('_eddn', 'name'),
        output_field=models.CharField(),
        db_persist=True,
    )

    objects = EddnManager()

    def clean(self) -> None:
        super().clean()
        if self._eddn != None:
            if self.__class__.objects.filter(_eddn=self._eddn).exclude(pk=self.pk).exists():
                raise ValidationError(
                    {'eddn': _('This value is already in use')}
                )
            
    class Meta:
        abstract = True
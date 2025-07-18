from django.db import models
from core.models import DateModels
from django.core.exceptions import ValidationError
from django.db.models.functions import Coalesce
from django.contrib import admin

from django.utils.translation import gettext_lazy as _

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

    def clean(self) -> None:
        super().clean()
        if self._eddn != None:
            if self.__class__.objects.filter(_eddn=self._eddn).exclude(pk=self.pk).exists():
                raise ValidationError(
                    {'eddn': _('This value is already in use')}
                )
            
    class Meta:
        abstract = True
from django.db import models

from django.utils.translation import gettext_lazy as _

from core.utility import get_values_list_or_default, get_or_none
from django.db import OperationalError, ProgrammingError

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


class AbstractDataEDDN(models.Model):
    """
    modelo astrato utilizato per unificare il salvatagio e la lettura dei dati
    che vengo utilizati per verificare e mapare i datti di eddn
    """
    _eddn = models.CharField(
        max_length=100, unique=True, 
        blank=True, null=True
    )

    @property
    def eddn(self) -> str:
        if self.__eddn:
            return self.__eddn
        return self.name
    eddn.fget.short_description = _('value for eddn')

    @eddn.setter
    def eddn(self, value: str) -> None:
        self.__eddn = value

    def get_data_list(self) -> list[str]:
        """
        ritorna una lista di modelli da usare per la mapatura e verivica dei datti ricevuti da EDDN
        """
        data = get_values_list_or_default(self.__class__, [], (OperationalError, ProgrammingError), '_eddn', 'name')
        x =  [data[0] if data[0] != None else data[1] for data in data]
        return x

    def get_instanze_from_eddn(self, eddn: str) -> models.Model:
        _eddn = get_or_none(self.__class__, _eddn=eddn)
        if _eddn:
            return _eddn
        return get_or_none(self.__class__, name=eddn)
        
    class Meta:
        abstract = True
from django.db import models
from django.utils.translation import gettext_lazy as _

class StarLuminosity(models.Model):
    """
    modello per la luminosita' delle stelle
    """
    name = models.CharField(
        max_length=255,
        verbose_name=_('name'),
        unique=True
    )
    note = models.TextField(
        verbose_name=_('note'),
        blank=True, null=True
    )
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('star luminosity')
        verbose_name_plural = _('star luminosities')
        
    
from django.db import models
from django.utils.translation import gettext_lazy as _

from eddn.models import AbstractDataEDDN

class Material(AbstractDataEDDN):
    """
    modello per i materiali
    """
    class MaterialType(models.TextChoices):
        """
        tipologia dei materiali
        """
        MANUFACTURED = 'ma', _('manufactured')
        RAW = 'ra', _('raw')
        ENCODED = 'en', _('encoded')

    class MaterialGrade(models.IntegerChoices):
        """
        grado dei materiali
        """
        VER_COMMON = 1, _('very common')
        COMMON = 2, _('common')
        STANDARD = 3, _('standard')
        RARE = 4, _('rare')
        VER_RARE = 5, _('very rare')

    name = models.CharField(
        max_length=255,
        verbose_name=_('name'),
        unique=True
    )
    type = models.CharField(
        max_length=2,
        choices=MaterialType.choices,
        verbose_name=_('type'),
    )
    grade = models.IntegerField(
        verbose_name=_('grade'),
        choices=MaterialGrade.choices,
    )
    note = models.TextField(
        verbose_name=_('note'),
        blank=True, null=True
    )
    
    def __str__(self):
        return self.name

    class Meta:
        indexes = [
            models.Index(fields=['type']),
            models.Index(fields=['grade']),
        ]
        verbose_name = _('material')
        verbose_name_plural = _('materials')
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.

from ed_economy.models import Economy
from ed_bgs.models.MinorFactionInSystem import MinorFactionInSystem

class System(models.Model):
    """
    modello deditatto al salvatagio dei dati generici riguardanti i sistemmi dati mode:
    nome, coordinata x, coordinata y, coordinata z, descrizione, data aggiornamento
    """
    class SecurityChoices(models.TextChoices):
        """
        valori possibili per la scema di sicurezza del sistema
        """
        Low = 'L', _('Low')
        Medium = 'M', _('Medium')
        High = 'H', _('High')
        Anarchy = 'A', _('Anarchy')

    name = models.CharField(
        max_length=100, unique=True, verbose_name=_('name')
    )
    x = models.FloatField(
        verbose_name=_('x coordinates'),
    )
    y = models.FloatField(
        verbose_name=_('y coordinates'),
    )
    z = models.FloatField(
        verbose_name=_('z coordinates'),
    )
    security = models.CharField(
        verbose_name=_('security'), max_length=1, 
        choices=SecurityChoices.choices, blank=True, null=True
    )
    population = models.PositiveIntegerField(
        verbose_name=_('population'), default=0
    )
    primaryEconomy = models.ForeignKey(
        Economy, on_delete=models.SET_NULL, 
        verbose_name=_('Primary economy'), blank=True, null=True,
        related_name='%(app_label)s_%(class)s_primary_related',
        related_query_name='%(app_label)s_%(class)ss_primary'
    )
    secondaryEconomy = models.ForeignKey(
        Economy, on_delete=models.SET_NULL, 
        verbose_name=_('Secondary economy'), blank=True, null=True,
        related_name='%(app_label)s_%(class)s_secondary_related',
        related_query_name='%(app_label)s_%(class)ss_secondary'
    )
    


    description = models.TextField(
        blank=True, null=True,
        verbose_name=_('description')
    )
    updated = models.DateTimeField(
        auto_now=True
    )

    @property
    def economy(self) -> list[Economy]:
        """
        ritorna l'economia della systema
        """
        if self.primaryEconomy == None and self.secondaryEconomy == None:
            return None
        elif self.secondaryEconomy == None:
            return [self.primaryEconomy]
        return [self.primaryEconomy, self.secondaryEconomy]
    economy.fget.short_description = _('economy')  

    def clean(self) -> None:
        if System.objects.filter(x=self.x, y=self.y, z=self.z).exclude(self).exists():
            raise ValidationError(_('a system with these coordinates already exists'))
        
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('System')
        verbose_name_plural = _('Systems')
        constraints = [
            models.UniqueConstraint(
                fields=['x','y',"z"], 
                name='unique_system_coordinates',
            )
        ]
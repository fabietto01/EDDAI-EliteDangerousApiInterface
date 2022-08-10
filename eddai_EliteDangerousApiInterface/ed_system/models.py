from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

# Create your models here.



class System(models.Model):
    """
    modello deditatto al salvatagio dei dati generici riguardanti i sistemmi dati mode:
    nome, coordinata x, coordinata y, coordinata z, descrizione, data aggiornamento
    """
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
    description = models.TextField(
        blank=True, null=True
    )
    updated = models.DateTimeField(
        auto_now=True
    )

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
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

class Ring(models.Model):
    """
    modello dedicato agli anelli atorno
    al pianeta
    """
    class RingType(models.TextChoices):
        """
        enumerazione per i tipi di anelli
        """
        METAL_RICH = 'MetalRich', _('Metal Rich')
        METALLIC = 'Metalic', _('Metalic')
        ROCKY = 'Rocky', _('Rocky')
        Icy = 'Icy', _('Icy')

    name = models.CharField(
        max_length=255,
        verbose_name=_('name'),
    )
    body = models.ForeignKey(
        'ed_body.BaseBody', models.CASCADE,
        verbose_name=_('body'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )
    innerRad = models.FloatField(
        verbose_name=_('inner radius'),
        help_text=_('inner radius of the ring'),
        validators=[
            MinValueValidator(0, _('the inner radius cannot be less than 0'))
        ],
        null=True, blank=True
    )
    outerRad = models.FloatField(
        verbose_name=_('outer radius'),
        help_text=_('outer radius of the ring'),
        validators=[
            MinValueValidator(0, _('the outer radius cannot be less than 0'))
        ],
        null=True, blank=True
    )
    massMT = models.FloatField(
        verbose_name=_('mass'),
        help_text=_('mass of the ring'),
        validators=[
            MinValueValidator(0, _('the mass cannot be less than 0'))
        ],
        null=True, blank=True
    )
    ringType = models.CharField(
        max_length=255,
        choices=RingType.choices,
        verbose_name=_('ring type'),
        help_text=_('type of the ring'),
    )

    def clean(self) -> None:
        if self.innerRad > self.outerRad:
            raise ValidationError(_('the inner radius cannot be greater than the outer radius'))
        super().clean()

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = _('ring')
        verbose_name_plural = _('rings')
        indexes = [
            models.Index(fields=['body']),
            models.Index(fields=['ringType']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['name', 'body'], name='unique_ring_name_body'),
            models.CheckConstraint(check=models.Q(innerRad__lt=models.F('outerRad'))  | models.Q(innerRad__isnull=True) | models.Q(outerRad__isnull=True), name='inner_radius_lt_outer_radius'),
        ]
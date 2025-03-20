from django.contrib.gis.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.contrib import admin
from django.db.models import Value
from django.db.models.functions import Concat

from .manager import SystemManager
from core.models import OwnerAndDateModels

from ed_economy.models import Economy
from ed_bgs.models.MinorFaction import MinorFaction
from ed_bgs.models.MinorFactionInSystem import MinorFactionInSystem

class System(OwnerAndDateModels, models.Model):
    """
        Represents a system in the Elite Dangerous universe.
        Attributes:
            name (CharField): The name of the system, unique and with a maximum length of 100 characters.
            coordinate (PointField): The 3D coordinates of the system, unique and using SRID 4979.
            security (CharField): The security level of the system, with choices defined in SecurityChoices.
            population (PositiveBigIntegerField): The population of the system, defaulting to 0.
            primaryEconomy (ForeignKey): The primary economy of the system, related to the Economy model.
            secondaryEconomy (ForeignKey): The secondary economy of the system, related to the Economy model.
            conrollingFaction (ForeignKey): The controlling faction of the system, related to the MinorFaction model.
            description (TextField): A textual description of the system, optional.
        Properties:
            economy (list[Economy]): Returns a list of the system's economies, combining primary and secondary economies.
        Methods:
            clean(): Validates that the controlling faction is present in the system.
            __str__(): Returns the name of the system.
        Meta:
            verbose_name (str): Human-readable name for the model.
            verbose_name_plural (str): Human-readable plural name for the model.
            constraints (list): List of constraints for the model.
            indexes (list): List of indexes for the model fields.
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
    address = models.BigIntegerField(
        verbose_name=_('address'), unique=True, 
    )
    coordinate = models.PointField(
        dim=3, srid=4979,
        verbose_name=_('coordinate'),
        unique=True,
    )
    security = models.CharField(
        verbose_name=_('security'), max_length=1, 
        choices=SecurityChoices.choices, blank=True, null=True
    )
    population = models.PositiveBigIntegerField(
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
    conrollingFaction = models.ForeignKey(
        MinorFaction, on_delete=models.SET_NULL,
        verbose_name=_('controlling faction'), blank=True, null=True,
        related_name='%(app_label)s_%(class)s_controlling_related',
        related_query_name='%(app_label)s_%(class)ss_controlling'
    )
    description = models.TextField(
        blank=True, null=True
    )

    objects = SystemManager()

    @property
    @admin.display(ordering=Concat("primaryEconomy", Value(" "), "secondaryEconomy"), description=_('economy'))
    def economy(self) -> list[Economy]:
        """
        Property that returns a list of economies for the system.

        This property combines the primary and secondary economies into a single list.
        If both primary and secondary economies are None, it returns None.
        If only the secondary economy is None, it returns a list containing only the primary economy.
        Otherwise, it returns a list containing both the primary and secondary economies.

        Returns:
            list[Economy] or None: A list of economies or None if both economies are not set.
        """
        if self.primaryEconomy == None and self.secondaryEconomy == None:
            return None
        elif self.secondaryEconomy == None:
            return [self.primaryEconomy]
        return [self.primaryEconomy, self.secondaryEconomy]

    def clean(self) -> None:
        if self.conrollingFaction != None:
            if not MinorFactionInSystem.objects.filter(system=self, minorFaction=self.conrollingFaction).exists():
                raise ValidationError(_('the controlling faction is not present in the system'))

    @staticmethod
    def get_distance(by, to) -> float:
        """
        Calculate the distance between two systems using the database via Distanza3D.
            Args:
                by (System): The system from which the distance is calculated.
                to (System): The system to which the distance is calculated.
            Returns:
                float: The distance between the two systems.
        """
        from django.contrib.gis.geos import Point
        from math import sqrt

        by_point:Point = by.coordinate
        to_point:Point = to.coordinate

        return round(sqrt(
            (by_point.x - to_point.x) ** 2 +
            (by_point.y - to_point.y) ** 2 +
            (by_point.z - to_point.z) ** 2
        ), 3)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = _('System')
        verbose_name_plural = _('Systems')
        constraints = [
            
        ]
        indexes = [
            models.Index(fields=['primaryEconomy', 'secondaryEconomy'], name='system_economy_idx'),
            models.Index(fields=['conrollingFaction'], name='system_controllingFaction_idx'),
            models.Index(fields=['security'], name='system_security_idx'),
        ]
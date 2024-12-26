from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from core.models import OwnerAndDateModels

from django.db.models import Q
from ed_system.models import System

class BaseBody(OwnerAndDateModels):
    """
    modello di base per le informazioni dei corpi celesti
    presenti al interno del systema

    query per order by

        SELECT * FROM `ed_info-dev`.ed_body_basebody as feat where system_id = 8158 order by 
        case
            when parentsID = 0
            then bodyID
            else (
                select bodyID
                from `ed_info-dev`.ed_body_basebody as parent
                where feat.parentsID = parent.bodyID and feat.system_id = parent.system_id
            ) 
        end asc
    """
    name = models.CharField(
        max_length=255,
        verbose_name=_('name'),
    )
    system = models.ForeignKey(
        System, models.CASCADE,
        verbose_name=_('system'),
        related_name='%(app_label)s_%(class)s_related',
        related_query_name='%(app_label)s_%(class)ss'
    )
    bodyID = models.PositiveIntegerField(
        verbose_name=_('body ID'),
    )
    parentsID = models.PositiveSmallIntegerField(
        default=0,
        verbose_name=_('parents ID'),
        help_text=_("enter the body ID of the object which orbit"),
        null=True
    )
    distance = models.FloatField(
        verbose_name=_('distance'),
        help_text=_('distance from the stary center'),
        validators=[
            MinValueValidator(0, _('the distance cannot be less than 0'))
        ],
        null=True
    )
    radius = models.FloatField(
        verbose_name=_('radius'),
        help_text=_('radius of the body'),
        validators=[
            MinValueValidator(0, _('the radius cannot be less than 0'))
        ],
        null=True, blank=True
    )
    surfaceTemperature = models.FloatField(
        verbose_name=_('surface temperature'),
        validators=[
            MinValueValidator(0, _('the surface temperature cannot be less than 0'))
        ],
        null=True, blank=True
    )
    #orbit parameters
    eccentricity = models.FloatField(
        verbose_name=_('eccentricity'),
        help_text=_('eccentricity of the orbit'),
        validators=[
            MinValueValidator(0, _('the eccentricity cannot be less than 0')),
            MaxValueValidator(1, _('the eccentricity cannot be greater than 1'))
        ],
        null=True, blank=True
    )
    orbitalInclination = models.FloatField(
        verbose_name=_('orbital inclination'),
        help_text=_('orbital inclination of the body'),
        validators=[
            MinValueValidator(-360, _('the orbital inclination cannot be less than -360')),
            MaxValueValidator(360, _('the orbital inclination cannot be greater than 360'))
        ],
        null=True, blank=True
    )
    orbitalPeriod = models.FloatField(
        verbose_name=_('orbital period'),
        help_text=_('orbital period of the body in days'),
        validators=[
            MinValueValidator(0, _('the orbital period cannot be less than 0'))
        ],
        null=True, blank=True
    )
    periapsis = models.FloatField(
        verbose_name=_('periapsis'),
        help_text=_('periapsis of the body'),
        null=True, blank=True
    )
    semiMajorAxis = models.FloatField(
        verbose_name=_('semi major axis'),
        help_text=_('semi major axis of the orbit'),
        validators=[
            MinValueValidator(0, _('the semi major axis cannot be less than 0'))
        ],
        null=True, blank=True
    )
    ascendingNode = models.FloatField(
        verbose_name=_('ascending node'),
        help_text=_('ascending node of the orbit'),
        null=True, blank=True
    )
    meanAnomaly = models.FloatField(
        verbose_name=_('mean anomaly'),
        help_text=_('mean anomaly of the orbit'),
        null=True, blank=True
    )
    #rotating
    axialTilt = models.FloatField(
        verbose_name=_('axial tilt'),
        help_text=_('axial tilt of the body'),
        validators=[
            MinValueValidator(-360, _('the axial tilt cannot be less than -360')),
            MaxValueValidator(360, _('the axial tilt cannot be greater than 360'))
        ],
        null=True, blank=True
    )
    rotationPeriod = models.FloatField(
        verbose_name=_('rotation period'),
        help_text=_('rotation period of the body in seconds'),
        null=True, blank=True
    )
    rotating = models.GeneratedField(
        verbose_name=_('rotating'),
        expression=Q(axialTilt__isnull=False) & Q(rotationPeriod__isnull=False),
        output_field=models.BooleanField(),
        db_persist=True,
    )
    orbiting = models.GeneratedField(
        verbose_name=_('orbiting'),
        expression=Q(eccentricity__isnull=False) & Q(orbitalInclination__isnull=False) & 
                   Q(orbitalPeriod__isnull=False) & Q(periapsis__isnull=False) & 
                   Q(semiMajorAxis__isnull=False),
        output_field=models.BooleanField(),
        db_persist=True,
    )

    def __str__(self):
        return self.name
    
    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        """
        Saves the current instance of the model. If validation fails, attempts to find a parent instance
        with the same name and system, and associates the current instance with the parent.
        Args:
            force_insert (bool): Whether to force an SQL INSERT. Defaults to False.
            force_update (bool): Whether to force an SQL UPDATE. Defaults to False.
            using (str): The database alias to use. Defaults to None.
            update_fields (list): A list of fields to update. Defaults to None.
        Raises:
            ValidationError: If validation fails and no suitable parent instance is found.
        Returns:
            None
        """

        def get_child_instance(parent:BaseBody):
            """
            Retrieve child instances of a given parent instance.

            This method iterates over the fields of the parent instance to find related child instances
            that are linked via one-to-one relationships. It collects these child instances in a list
            and checks if an instance of the same class as the parent exists.

            Args:
                parent (BaseBody): The parent instance from which to retrieve child instances.

            Returns:
                tuple: A tuple containing:
                    - childList (list): A list of child instances related to the parent.
                    - exist (bool): A boolean indicating whether an instance of the same class as the parent exists.
            """
            childList = []
            exist = False
            for filds in parent._meta.get_fields():
                if filds.one_to_one and filds.parent_link:
                    try:
                        child = getattr(parent, filds.name)
                        if child.__class__ != self.__class__:
                            childList.append(child)
                        elif child.__class__ == self.__class__ and child.id == parent.id:
                            exist = True
                            break
                    except filds.related_model.DoesNotExist:
                        pass
            return childList, exist

        try:
            self.validate_constraints()
            super().save(force_insert, force_update, using, update_fields)
        except ValidationError as e:
            try:
                parent = BaseBody.objects.get(name=self.name, system=self.system)
                childList, exist = get_child_instance(parent)
                if parent and (not childList) and (not exist):
                    self.basebody_ptr = parent
                    self.basebody_ptr_id = parent.id
                    try:
                        if not self.created_by:
                            self.created_by = parent.created_by
                            self.created_by_id = parent.created_by.id
                    except BaseBody.created_by.RelatedObjectDoesNotExist:
                        self.created_by = parent.created_by
                        self.created_by_id = parent.created_by.id
                    if not self.created_at:
                        self.created_at = parent.created_at
                    super().save(force_insert, force_update, using, update_fields)
                else:
                    raise e
            except BaseBody.DoesNotExist:
                raise e
        
    class Meta:
        verbose_name = _('body')
        verbose_name_plural = _('bodies')
        indexes = [
            models.Index(fields=['system']),
            models.Index(fields=['bodyID']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['name','system'], name='unique_body_in_system'),
            models.UniqueConstraint(fields=['bodyID','system'], name='unique_bodyID_in_system'),
        ]

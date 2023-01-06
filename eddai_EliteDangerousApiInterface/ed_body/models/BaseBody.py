from django.db import models
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

from ed_system.models import System


class BaseBody(models.Model):
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
    updated = models.DateTimeField(
        auto_now=True
    )

    @property
    def rotating(self) -> bool:
        return bool(self.axialTilt and self.rotationPeriod)
    rotating.fget.short_description = _('rotating') 

    @property
    def orbiting(self) -> bool:
        return bool(
            self.eccentricity and self.orbitalInclination and 
            self.orbitalPeriod and self.periapsis and self.semiMajorAxis
        )
    orbiting.fget.short_description = _('orbiting') 

    def __str__(self):
        return self.name

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None) -> None:
        """
        method overriding to avoid the error when the parent is already present in 
        the db and you want to add the child
        """

        def str_in_list(string: str, list: list) -> bool:
            """
            check if one of the strings in the list is present in the string
            """
            for item in list:
                if item in string:
                    return True
            return False

        def get_child_instance(parent):
            """
            get the child instance of the parent
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
            super().save(force_insert, force_update, using, update_fields)
        except IntegrityError as e:
            if str_in_list(str(e), [c.name for c in BaseBody._meta.constraints]) and self.__class__ != BaseBody.__class__:
                try:
                    parent = BaseBody.objects.get(name=self.name, system=self.system, bodyID=self.bodyID)
                    childList, exist = get_child_instance(parent)
                    if parent and (not childList) and (not exist):
                        self.basebody_ptr = parent
                        self.basebody_ptr_id = parent.id
                        return super().save(force_insert, force_update, using, update_fields)
                except BaseBody.DoesNotExist:
                    raise e
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

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings

AUTH_USER_MODEL = settings.AUTH_USER_MODEL

class OwnerModels(models.Model):
    """
    abstract model for the creation and update user of the model
    """

    created_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, 
        related_name='%(app_label)s_%(class)s_created', 
        verbose_name=_('Created by')
    )
    updated_by = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, 
        related_name='%(app_label)s_%(class)s_updated',
        verbose_name=_('Updated by')
    )
    
    class Meta:
        abstract = True

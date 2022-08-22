from django.db import models
from django.utils.translation import gettext_lazy as _

class MinorFaction(models.Model):
    """
    
    """
    name = models.CharField(
        max_length=255, unique=True, verbose_name=_('name')
    )
    allegiance = None
    government = None
    
    
    updated = models.DateTimeField(
        auto_now=True
    )
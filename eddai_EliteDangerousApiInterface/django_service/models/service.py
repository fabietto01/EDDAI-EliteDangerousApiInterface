from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class Service(models.Model):
    
    class StatusChoices(models.TextChoices):
        RUN = 'r', _("RUN")
        STOP = 's', _("STOP") 
        ERROR = 'e', _("ERROR")
        
        __empty__ = _("(Unknown)")
    
    pk = models.CharField(
        verbose_name=_("Service"),
        max_length=100, primary_key=True, unique=True
    )
    status = models.CharField(
        max_length=1,
        choices=StatusChoices.choices
    )
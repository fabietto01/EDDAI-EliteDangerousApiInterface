from django.db import models
from django.db.models.functions import Coalesce

class EddnManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().annotate(
             eddn=Coalesce('_eddn', 'name')
        )
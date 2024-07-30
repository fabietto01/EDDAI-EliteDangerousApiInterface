from django.db import models
from django.utils.translation import gettext_lazy as _

class DateModels(models.Model):
    """
    abstract model for the creation and update date of the model
    """

    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_('Created')
    )
    updated_at = models.DateTimeField(
        auto_now=True, verbose_name=_('Updated')
    )

    class Meta:
        abstract = True
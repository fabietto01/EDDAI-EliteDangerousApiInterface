from django.db import models
from django.utils.translation import gettext_lazy as _

from .dateModels import DateModels
from .ownerModels import OwnerModels

class OwnerAndDateModels(OwnerModels, DateModels):
    """
    abstract model for the creation and update user and date of the model
    """

    class Meta:
        abstract = True
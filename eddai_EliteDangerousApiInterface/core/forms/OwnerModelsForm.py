from typing import Any
from ..models import OwnerModels
from django.forms import ModelForm

class OwnerModelsForm(ModelForm):
    
    class Meta:
        exlude = ['created_by', 'updated_by']
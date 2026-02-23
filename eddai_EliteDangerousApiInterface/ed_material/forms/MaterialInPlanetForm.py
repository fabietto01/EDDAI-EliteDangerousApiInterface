from django import forms
from django.utils.translation import gettext_lazy as _
from core.admin import BaseOwnerModelsInlineModelAdmin
from ed_material.models import Material, MaterialInPlanet

class MaterialInPlanetForm(BaseOwnerModelsInlineModelAdmin.BaseOwnerModelsTabularInlineModelForm):

    material  = forms.ModelChoiceField(
        queryset=Material.objects.filter(type=Material.MaterialType.RAW.value),
    )

    class Meta:
        model = MaterialInPlanet
        fields = ('planet', 'material', 'percent')
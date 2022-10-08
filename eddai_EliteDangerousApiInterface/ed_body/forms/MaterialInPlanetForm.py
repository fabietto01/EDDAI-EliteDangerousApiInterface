from django import forms
from django.utils.translation import gettext_lazy as _

from ed_body.models import MaterialInPlanet
from ed_material.models.Material import Material

class MaterialInPlanetForm(forms.ModelForm):

    material  = forms.ModelChoiceField(
        queryset=Material.objects.filter(type=Material.MaterialType.RAW.value),
    )

    class Meta:
        model = MaterialInPlanet
        fields = ('planet', 'material', 'percent')
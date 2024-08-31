from django import forms
from ed_system.models import System
from ed_system.widget import Point3DWidget

class SystemModelForm(forms.ModelForm):

    class Meta:
        model = System
        fields = '__all__'
        widgets = {
            'coordinate': Point3DWidget
        }
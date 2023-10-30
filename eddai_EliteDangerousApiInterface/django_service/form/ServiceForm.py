from django import forms
from django.utils.translation import gettext_lazy as _

from ..celey.utility import get_servis_list, get_app

from ..models import Service

class ServiceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs) -> None:
        super(ServiceForm, self).__init__(*args, **kwargs)
        app = get_app()
        self.fields['task'].choices = [
            (task_name, task_name) for task_name in get_servis_list(app)
        ]

    task = forms.ChoiceField()

    class Meta:
        model = Service
        fields = '__all__'
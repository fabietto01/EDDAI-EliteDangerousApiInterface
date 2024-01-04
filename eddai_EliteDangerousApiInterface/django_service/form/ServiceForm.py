from django import forms
from django.utils.translation import gettext_lazy as _

from ..celery import app
from ..celery.Service.utility import get_servis_list

from ..models import Service

class ServiceForm(forms.ModelForm):

    def __init__(self, *args, **kwargs) -> None:
        super(ServiceForm, self).__init__(*args, **kwargs)
        self.fields['service'].choices = [
            (task_name, task_name) for task_name in get_servis_list(app)
        ]

    service = forms.ChoiceField()

    class Meta:
        model = Service
        fields = '__all__'
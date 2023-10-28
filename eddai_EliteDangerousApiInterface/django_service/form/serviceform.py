from django import forms
from django.utils.translation import gettext_lazy as _

from ..models import Service, ServiceEvent as Event
from .Widget import TableSelect

class ServiceForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs) -> None:
        super(ServiceForm, self).__init__(*args, **kwargs)
        self.fields['related_name'].queryset = Event.objects.filter(
            service=getattr(self, 'instance', None)
        )[:10]

    related_name = forms.ModelMultipleChoiceField(
        queryset=None, widget=TableSelect(fields=["event", "created"]), 
        required=False, 
    )
    #widget=SelectMultiple

    class Meta:
        model = Service
        fields = '__all__'
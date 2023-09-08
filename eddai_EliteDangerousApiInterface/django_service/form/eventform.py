from django.forms import ModelForm

from ..models import ServiceEvent as Event

class EventForm(ModelForm):
        
        class Meta:
            model = Event
            fields = '__all__'
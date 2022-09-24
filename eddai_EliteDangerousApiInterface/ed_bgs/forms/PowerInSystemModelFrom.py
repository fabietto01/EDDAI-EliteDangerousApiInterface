from django.forms import ModelForm
from ed_bgs.models import PowerInSystem
from django.utils.translation import gettext_lazy as _

from django.core.exceptions import ValidationError

class PowerInSystemForm(ModelForm):

    def clean(self):
        powers = self.cleaned_data.get('power')
        if powers.count() > PowerInSystem.MaxRelation or powers.count() == 0:
            raise ValidationError(_('You can select only 1 or 2 powers'))
        state = self.cleaned_data.get('state')
        if state.name in PowerInSystem.StateForMoreRellation and powers.count() < 2:
            raise ValidationError(_('You can select only 2 powers for this state'))
        elif not state.name in PowerInSystem.StateForMoreRellation and powers.count() > 1 :
            raise ValidationError(_('You can select only 1 power for this state'))
        return super().clean()

    class Meta:
        model = PowerInSystem
        fields = ('system', 'powers', 'state')
from django.db.models import Model
from django.utils.translation import gettext_lazy as _
from django_filters.filters import EMPTY_VALUES
from core.api.fields import CacheSlugRelatedField
import re

class HappinessCacheSlugRelatedField(CacheSlugRelatedField):
    default_error_messages = {
        'invalid_choice': _('"{input}" is not a valid choice.'),
        'incorrect_format': _('"{input}" Incorrect format'),
        'state_phase': _('"{input}" is not a valid phase state'),
    }

    def to_internal_value(self, data) -> dict[Model, int]:
        if data.__class__ != dict:
            if data == '' and self.allow_blank:
                return ''
            regex = r'Faction_([a-zA-Z]{1,})Band([0-9]);$'
            if re.match(regex, data):
                self.fail('incorrect_format', input=data)
        
            reg = re.findall(regex, data)
            happi = str(reg[0][0]) if reg else None
            statePhase = int(reg[0][1]) if reg else None
        else:
            happi, statePhase = data.get('State'), data.get('StatePhase')

        if not 0 < statePhase < 4:
            self.fail('state_phase', input=statePhase)
        
        try:
            return {
                'State': super().to_internal_value(happi),
                'StatePhase': statePhase,
            }
        except KeyError:
            self.fail('invalid_choice', input=happi)
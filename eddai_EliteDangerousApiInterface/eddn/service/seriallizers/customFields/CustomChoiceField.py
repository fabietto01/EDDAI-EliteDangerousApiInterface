from pickle import EMPTY_LIST
from django.utils.translation import gettext_lazy as _
from typing import Type
from rest_framework import serializers
from django_filters.filters import EMPTY_VALUES
import re

class CustomChoiceField(serializers.ChoiceField):
    def to_internal_value(self, data):
        if not data in EMPTY_VALUES:
            reg = re.findall(r'_([a-zA-Z]{1,});$', data)
            data = str(reg[0]) if reg else None
        return super().to_internal_value(data)

class HappinessChoiceField(serializers.ChoiceField):
    default_error_messages = {
        'invalid_choice': _('"{input}" is not a valid choice.'),
        'incorrect_format': _('"{input}" Incorrect format'),
        'state_configuration': _('"{input}" is not a valid configuration state'),
    }

    def to_internal_value(self, data):
        if data.__class__ != tuple:
            if data == '' and self.allow_blank:
                return ''
            regex = r'Faction_([a-zA-Z]{1,})Band([0-9]);$'
            if re.match(regex, data):
                self.fail('incorrect_format', input=data)
        
            reg = re.findall(regex, data)
            happi = str(reg[0][0]) if reg else None
            HappiStato = int(reg[0][1]) if reg else None
        else:
            happi, HappiStato = data

        if not 0 < HappiStato < 4:
            self.fail('state_configuration', input=HappiStato)
        
        try:
            return (self.choice_strings_to_values[str(happi)], HappiStato)
        except KeyError:
            self.fail('invalid_choice', input=happi)

    def to_representation(self, value):
        if value in EMPTY_VALUES:
            return value
        return f"$Faction_{value[0]}Band{value[1]};"
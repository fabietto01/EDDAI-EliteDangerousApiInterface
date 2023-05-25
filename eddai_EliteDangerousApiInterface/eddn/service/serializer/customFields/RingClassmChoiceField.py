from rest_framework import serializers
from django_filters.filters import EMPTY_VALUES
import re

class RingClassmChoiceField(serializers.ChoiceField):
    def to_internal_value(self, data):
        if (not data in EMPTY_VALUES) and (not data in  self.choice_strings_to_values.keys()):
            reg = re.findall(r'eRingClass_([a-zA-Z]{1,})$', data)
            data = str(reg[0]) if reg else ''
        return super().to_internal_value(data)
   
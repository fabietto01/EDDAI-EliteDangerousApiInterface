from rest_framework import serializers
from django_filters.filters import EMPTY_VALUES
from ed_mining.models import Ring

import re

class RingTypeChoiceField(serializers.ChoiceField):

    def __init__(self, **kwargs):
        choices = Ring.RingType.choices
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data: dict):
        if not data in EMPTY_VALUES:
            reg = re.findall(r'eRingClass_([a-zA-Z]{1,})$', data)
            data = str(reg[0]) if reg else ''
        return super().to_internal_value(data)
    
    def to_representation(self, value: str) -> str:
        value = super().to_representation(value)
        return f'eRingClass_{value}' if value else ''
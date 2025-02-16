from rest_framework import serializers
from django_filters.filters import EMPTY_VALUES
import re

from ed_system.models import System

class SystemSecurityChoiceField(serializers.ChoiceField):

    def __init__(self, **kwargs):
        choices = System.SecurityChoices.choices
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data):
        if not data in EMPTY_VALUES:
            reg = re.findall(r'_([a-zA-Z]{1,});$', data)
            data = str(reg[0]) if reg else ''
            data = data[:1].upper() if data != 'None' else ''
        return super().to_internal_value(data)
from pickle import EMPTY_LIST
from rest_framework import serializers
from django_filters.filters import EMPTY_VALUES
import re

class CustomChoiceField(serializers.ChoiceField):
    def to_internal_value(self, data):
        if not data in EMPTY_VALUES:
            reg = re.findall(r'_([a-zA-Z]{1,});$', data)
            data = str(reg[0]) if reg else None
        return super().to_internal_value(data)
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from django_filters.filters import EMPTY_VALUES
import re

class CustomChoiceField(serializers.ChoiceField):
    def to_internal_value(self, data):
        if not data in EMPTY_VALUES:
            reg = re.findall(r'_([a-zA-Z]{1,});$', data)
            data = str(reg[0]) if reg else ''
            data = data if data != 'None' else ''
        return super().to_internal_value(data)
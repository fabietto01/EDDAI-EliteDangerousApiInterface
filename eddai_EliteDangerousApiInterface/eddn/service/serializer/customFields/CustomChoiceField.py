from rest_framework import serializers
from .BaseCustinField import BaseCustomField

from enum import Enum

class CustomChoiceField(serializers.ChoiceField, BaseCustomField):
    
    def run_validation(self, data):
        data = BaseCustomField._to_internal_value(self, data)
        return super().run_validation(data)
    
    def to_internal_value(self, data):
        if data == '' and self.allow_blank:
            return ''
        if isinstance(data, Enum) and str(data) != str(data.value):
            data = data.value
        try:
            return self.choice_strings_to_values[str(data)]
        except KeyError:
            self.fail('invalid_choice', input=data)
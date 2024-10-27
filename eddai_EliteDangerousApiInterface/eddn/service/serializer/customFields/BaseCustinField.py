from rest_framework.fields import empty
from rest_framework.serializers import Field
from django_filters.filters import EMPTY_VALUES
import re

class BaseCustomField(Field):

    def _to_internal_value(self, data):
        if not data in EMPTY_VALUES:
            reg = re.findall(r'_([a-zA-Z]{1,});$', data)
            data = str(reg[0]) if reg else ''
            data = data if data != 'None' else ''
        return data
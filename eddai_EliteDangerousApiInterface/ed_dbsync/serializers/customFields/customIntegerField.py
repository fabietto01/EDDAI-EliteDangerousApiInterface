from rest_framework.serializers import IntegerField, FloatField, DecimalField

from django.utils.encoding import smart_str

class CustomIntegerField(IntegerField):
    """
    A custom IntegerField that allows empty values and returns a default value if the value is empty.
    """

    def validate_empty_values(self, data):
        if smart_str(data).strip() == '' and self.allow_null:
            return (True, self.get_default())
        return super().validate_empty_values(data)

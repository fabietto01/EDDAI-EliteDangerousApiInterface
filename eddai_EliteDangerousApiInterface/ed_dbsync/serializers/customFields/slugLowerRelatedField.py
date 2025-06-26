from rest_framework import serializers
from django.db.models.functions import Lower


class SlugLowerRelatedField(serializers.SlugRelatedField):
    """
    A SlugRelatedField that converts the input to lowercase before validation.
    """

    def __init__(self, slug_field, queryset, **kwargs):
        annotated_slug_field = f"{slug_field}_lower"
        queryset = queryset.annotate(**{annotated_slug_field: Lower(slug_field)})
        super().__init__(slug_field=annotated_slug_field, queryset=queryset, **kwargs)
       
    def to_internal_value(self, data):
        data = data.lower()
        return super().to_internal_value(data)
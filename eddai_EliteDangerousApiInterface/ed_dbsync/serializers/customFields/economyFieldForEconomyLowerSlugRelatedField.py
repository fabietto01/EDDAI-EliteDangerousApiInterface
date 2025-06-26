from rest_framework import serializers

from ed_economy.models import Economy

class EconomyFieldForEconomyLowerSlugRelatedField(serializers.SlugRelatedField):

    def __init__(self, slug_field=None, **kwargs):
        queryset = Economy.objects.all()
        super().__init__(slug_field=slug_field, queryset=queryset, **kwargs)

    def to_internal_value(self, data):
        data = f"$economy_{data};"
        return super().to_internal_value(data)
    
    def to_representation(self, value):
        value = super().to_representation(value)
        return value.replace("$economy_", "").replace(";", "")

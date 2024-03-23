from rest_framework.serializers import ChoiceField


class CacheCharField(ChoiceField):

    def to_internal_value(self, data):
        return super().to_internal_value(data)

    def to_representation(self, value):
        return super().to_representation(value)
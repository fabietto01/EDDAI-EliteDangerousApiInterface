from rest_framework import serializers

class ReserveLevelChoiceField(serializers.ChoiceField):
    def to_internal_value(self, data):
        if str(data).endswith('Resources'):
            data = data[:-9]
        return super().to_internal_value(data)
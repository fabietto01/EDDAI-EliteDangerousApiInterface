from rest_framework import serializers

from ed_body.models import Planet

class ReserveLevelChoiceField(serializers.ChoiceField):

    def __init__(self, *args, **kwargs):
        choices=Planet.ReserveLevel.choices
        super().__init__(choices=choices, *args, **kwargs)

    def to_internal_value(self, data):
        if str(data).endswith('Resources'):
            data = data[:-9]
        return super().to_internal_value(data)
    
    def to_representation(self, value):
        value = super().to_representation(value)
        return f'{value}Resources'
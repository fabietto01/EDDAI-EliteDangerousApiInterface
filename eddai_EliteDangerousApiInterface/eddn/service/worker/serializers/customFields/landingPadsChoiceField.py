from rest_framework import serializers
from django_filters.filters import EMPTY_VALUES
from ed_station.models import Station

class LandingPadsChoiceField(serializers.ChoiceField):

    def __init__(self, **kwargs):
        choices = Station.LandingPadChoices.names
        super().__init__(choices=choices, **kwargs)

    def to_internal_value(self, data: dict):
        choices = Station.LandingPadChoices.__empty__

        if data.__class__ != dict:
            if data in EMPTY_VALUES:
                return choices
            
        if data.get(Station.LandingPadChoices.Large.name, 0) > 0:
            choices = Station.LandingPadChoices.Large
        elif data.get(Station.LandingPadChoices.Medium.name, 0) > 0:
            choices = Station.LandingPadChoices.Medium
        elif data.get(Station.LandingPadChoices.Small.name, 0) > 0:
            choices = Station.LandingPadChoices.Small

        return choices
    
    def to_representation(self, value: Station.LandingPadChoices) -> dict:
        return {
            Station.LandingPadChoices.Large.name: value == Station.LandingPadChoices.Large,
            Station.LandingPadChoices.Medium.name: value == Station.LandingPadChoices.Medium,
            Station.LandingPadChoices.Small.name: value == Station.LandingPadChoices.Small,
        }
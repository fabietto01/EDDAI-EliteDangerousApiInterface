from ed_core.api.filters.baseDistanceFilterSet import BaseDistanceFilterSet
from ed_system.models import System

class SystemFilterSet(BaseDistanceFilterSet):
    """
    SystemFilterSet is a filter set for the System model, inheriting from BaseDistanceFilterSet.
    It allows filtering of systems based on various fields such as security, population, primaryEconomy, secondaryEconomy, and controllingFaction.
    Attributes:
        distance_field (str): The field used for distance calculations, set to 'coordinate'.
    Meta:
        model (System): The model to filter.
        fields (dict): A dictionary specifying the fields to filter on and the types of filtering allowed.
            - 'security': Allows exact matching.
            - 'population': Allows exact matching, less than, and greater than comparisons.
            - 'primaryEconomy': Allows exact matching.
            - 'secondaryEconomy': Allows exact matching.
            - 'controllingFaction': Allows exact matching.
    """
    
    distance_field = 'coordinate'

    class Meta:
        model = System
        fields = {
            'security': ['exact',],
            'population': ['exact', 'lt', 'gt'],
            'primaryEconomy': ['exact',],
            'secondaryEconomy': ['exact',],
            'conrollingFaction': ['exact',],
        }
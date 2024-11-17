from django_filters.rest_framework import FilterSet
from ed_system.models import System

from rest_framework_gis.filters import DistanceToPointFilter

class SystemFilterSet(FilterSet):
    """
    filter for system model
    """

    class Meta:
        model = System
        fields = {
            'name': ['exact',],
            'security': ['exact',],
            'population': ['exact', 'lt', 'gt'],
            'primaryEconomy': ['exact',],
            'secondaryEconomy': ['exact',],
            'conrollingFaction': ['exact',],
        }
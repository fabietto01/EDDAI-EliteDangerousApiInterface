import django_filters
from django.utils.translation import gettext_lazy as _

from django_filters.constants import EMPTY_VALUES

from ed_core.api.filters.baseDistanceFilterSet import BaseDistanceFilterSet

from drf_spectacular.utils import extend_schema_field
from drf_spectacular.types import OpenApiTypes

from ed_system.manager import SystemQuerySet
from ed_system.models import System
from ed_bgs.models import (
    MinorFaction, State, Power,
    Faction, Government
)

class SystemFilterSet(BaseDistanceFilterSet):
    """
    SystemFilterSet is a filter set for the System model, inheriting from BaseDistanceFilterSet.
    It allows filtering of systems based on various fields such as security, population, primaryEconomy, secondaryEconomy, and conrollingFaction.
    Attributes:
        distance_field (str): The field used for distance calculations, set to 'coordinate'.
    Meta:
        model (System): The model to filter.
        fields (dict): A dictionary specifying the fields to filter on and the types of filtering allowed.
            - 'security': Allows exact matching.
            - 'population': Allows exact matching, less than, and greater than comparisons.
            - 'primaryEconomy': Allows exact matching.
            - 'secondaryEconomy': Allows exact matching.
            - 'conrollingFaction': Allows exact matching.
    """
    
    distance_field = 'coordinate'
    default_ordering = ['name']

    @extend_schema_field(OpenApiTypes.INT)
    def filter_conrollingFaction_state(self, queryset:SystemQuerySet, name, value):
        """
        Filter the queryset by the state of the controlling faction
        """
        if value not in EMPTY_VALUES:
            return queryset.view_system_control_faction().filter(
                conrolling_faction_view__ed_bgs_stateinminorfactions__state=value
            )
        return queryset
    
    @extend_schema_field(OpenApiTypes.INT)
    def filter_conrollingFaction_not_state(self, queryset:SystemQuerySet, name, value):
        """
        Filter the queryset by the state of the controlling faction
        """
        if value not in EMPTY_VALUES:
            return queryset.view_system_control_faction().exclude(
                conrolling_faction_view__ed_bgs_stateinminorfactions__state=value
            )
        return queryset
    
    @extend_schema_field(OpenApiTypes.INT)
    def filter_conrollingFaction_in_state(self, queryset:SystemQuerySet, name, value):
        """
        Filter the queryset by the state of the controlling faction
        """
        if value not in EMPTY_VALUES and value:
            return queryset.view_system_control_faction().filter(
                conrolling_faction_view__ed_bgs_stateinminorfactions__state__in=value
            )
        return queryset
    
    @extend_schema_field(OpenApiTypes.INT)
    def  filter_conrollingFaction_not_in_state(self, queryset:SystemQuerySet, name, value):
        """
        Filter the queryset by the state of the controlling faction"
        """
        if value not in EMPTY_VALUES and value:
            return queryset.view_system_control_faction().exclude(
                conrolling_faction_view__ed_bgs_stateinminorfactions__state__in=value
            )
        return queryset

    conrollingFaction__not = django_filters.ModelChoiceFilter(
        queryset=MinorFaction.objects.all(),
        field_name='conrollingFaction',
        lookup_expr='exact',
        label=_('Not Controlling Faction'),
        exclude=True
    )
    conrollingFaction__state = django_filters.ModelChoiceFilter(
        queryset=State.objects.all(),
        method='filter_conrollingFaction_state',
        label=_('The controlling faction is in the state'),
    )
    conrollingFaction__not__state = django_filters.ModelChoiceFilter(
        queryset=State.objects.all(),
        method='filter_conrollingFaction_not_state',
        label=_('The controlling faction does not have the status'),
    )
    conrollingFaction__in__state = django_filters.ModelMultipleChoiceFilter(
        queryset=State.objects.all(),
        method='filter_conrollingFaction_in_state',
        label=_('The controlling faction is in a state'),
    )
    conrollingFaction__not__in__state = django_filters.ModelMultipleChoiceFilter(
        queryset=State.objects.all(),
        method='filter_conrollingFaction_not_in_state',
        label=_('The controlling faction is not in a state'),
    )
    power = django_filters.ModelChoiceFilter(
        queryset=Power.objects.all(),
        field_name='ed_bgs_powerinsystems__power',
        lookup_expr='exact',
        label=_('Power'),
    )
    allegiance = django_filters.ModelChoiceFilter(
        queryset=Faction.objects.all(),
        field_name='conrollingFaction__allegiance',
        lookup_expr='exact',
        label=_('Allegiance'),
    )
    government = django_filters.ModelChoiceFilter(
        queryset=Government.objects.all(),
        field_name='conrollingFaction__government',
        lookup_expr='exact',
        label=_('Allegiance'),
    )

    class Meta:
        model = System
        fields = {
            'security': ['exact',],
            'population': ['exact', 'lt', 'gt'],
            'primaryEconomy': ['exact','in'],
            'secondaryEconomy': ['exact','in'],
            'conrollingFaction': ['exact', 'in'],
            'created_at': ['exact', 'lt', 'gt'],
            'updated_at': ['exact', 'lt', 'gt'],
        }
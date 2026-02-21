import django_filters

from ed_bgs.models import State

class StateFilterSet(django_filters.FilterSet):

    type = django_filters.TypedMultipleChoiceFilter(
        field_name='type',
        choices=State.TypeChoices.choices,
    )

    class Meta:
        model = State
        fields = ['type']
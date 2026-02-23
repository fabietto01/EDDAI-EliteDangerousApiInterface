import django_filters

from ed_bgs.models import Government

class GovernmentFilterSet(django_filters.FilterSet):

    type = django_filters.TypedMultipleChoiceFilter(
        field_name='type',
        choices=Government.TipeChoices.choices,
    )

    class Meta:
        model = Government
        fields = ['type']
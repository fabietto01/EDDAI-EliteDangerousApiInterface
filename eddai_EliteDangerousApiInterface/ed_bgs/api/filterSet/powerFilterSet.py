import django_filters

from ed_bgs.models import Power, Faction

class PowerFilterSet(django_filters.FilterSet):

    allegiance = django_filters.ModelChoiceFilter(
        queryset=Faction.objects.all(),
    )

    class Meta:
        model = Power
        fields = ['allegiance']
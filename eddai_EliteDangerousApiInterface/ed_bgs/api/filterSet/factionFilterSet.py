import django_filters

from ed_bgs.models import Faction, Government


class FactionFilterSet(django_filters.FilterSet):

    government = django_filters.ModelChoiceFilter(
        field_name='government',
        queryset=Government.objects.all()
    )
    
    class Meta:
        model = Faction
        fields = ['government']

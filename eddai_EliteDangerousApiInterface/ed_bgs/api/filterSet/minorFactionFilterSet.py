import django_filters

from ed_bgs.models import MinorFaction, Faction, Government

class MinorFactionFilterSet(django_filters.FilterSet):

    allegiance = django_filters.ModelChoiceFilter(
        field_name='allegiance',
        queryset=Faction.objects.all()
    )

    government = django_filters.ModelChoiceFilter(
        field_name='government',
        queryset=Government.objects.all()
    )
    
    class Meta:
        model = MinorFaction
        fields = ['allegiance', 'government']
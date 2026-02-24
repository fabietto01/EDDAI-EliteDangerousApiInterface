import django_filters

from ed_bgs.models import MinorFactionInSystem, MinorFaction
from ed_system.models import System


class MinorFactionInSystemFilterSet(django_filters.FilterSet):

    system = django_filters.ModelChoiceFilter(
        field_name='system',
        queryset=System.objects.all()
    )

    minorFaction = django_filters.ModelChoiceFilter(
        field_name='minorFaction',
        queryset=MinorFaction.objects.all()
    )
    
    Influence = django_filters.RangeFilter(
        field_name='Influence',
    )
    
    class Meta:
        model = MinorFactionInSystem
        fields = ['system', 'minorFaction', 'Influence']

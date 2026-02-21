import django_filters

from ed_bgs.models import PowerInSystem, Power, PowerState
from ed_system.models import System


class PowerInSystemFilterSet(django_filters.FilterSet):

    system = django_filters.ModelChoiceFilter(
        field_name='system',
        queryset=System.objects.all()
    )

    power = django_filters.ModelChoiceFilter(
        field_name='power',
        queryset=Power.objects.all()
    )

    state = django_filters.ModelChoiceFilter(
        field_name='state',
        queryset=PowerState.objects.all()
    )
    
    class Meta:
        model = PowerInSystem
        fields = ['system', 'power', 'state']

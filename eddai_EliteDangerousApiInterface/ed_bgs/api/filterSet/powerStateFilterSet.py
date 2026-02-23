import django_filters

from ed_bgs.models import PowerState


class PowerStateFilterSet(django_filters.FilterSet):
    """FilterSet for PowerState model."""
    
    class Meta:
        model = PowerState
        fields = ['name']

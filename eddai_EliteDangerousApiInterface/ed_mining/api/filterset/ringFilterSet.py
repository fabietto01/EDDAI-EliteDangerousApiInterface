import django_filters

from ed_core.api.filters.baseDistanceFilterSet import BaseDistanceFilterSet
from django.utils.translation import gettext_lazy as _

from ed_mining.models import Ring, HotspotType

class RingFilterSet(BaseDistanceFilterSet):

    distance_field = 'body__system__coordinate'
    default_ordering = 'name'

    hotspot_type = django_filters.ModelMultipleChoiceFilter(
        queryset=HotspotType.objects.all(),
        field_name='ed_mining_hotspots__type__name',
        label=_('Hotspot Type'),
        lookup_expr='exact',
    )

    class Meta:
        model = Ring
        fields = {
            'name': ['exact'],
            'body': ['exact'],
            'ringType': ['exact', "in"],
        }
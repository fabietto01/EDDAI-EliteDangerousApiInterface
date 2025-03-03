import django_filters

from ed_core.api.filters.baseDistanceFilterSet import BaseDistanceFilterSet
from django.utils.translation import gettext_lazy as _

from ed_mining.models import Ring

class RingFilterSet(BaseDistanceFilterSet):

    distance_field = 'body__system__coordinate'
    default_ordering = 'name'

    class Meta:
        model = Ring
        fields = {
            'name': ['exact'],
            'body': ['exact'],
            'ringType': ['exact', "in"],
        }
import django_filters
from .baseBodyFilterSet import BaseBodyFilterSet

from ed_body.models import Planet
from ed_mining.models import Ring

class PlanetFilterSet(BaseBodyFilterSet):

    ring_type = django_filters.ChoiceFilter(
        field_name='ed_mining_rings__ringType',
        choices=Ring.RingType.choices,
        label='Ring type'
    )

    class Meta:
        model = Planet
        fields = {
            'name': ['exact'],
            'system': ['exact'],
            'distance': ['lt', 'lte', 'gt', 'gte'],
            'atmosphereType': ['exact'],
            'planetType': ['exact'],
            'volcanism': ['exact'],
            'terraformState': ['exact'],
            'landable': ['exact'],
            'reserveLevel': ['exact'],
        }
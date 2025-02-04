from .baseBodyFilterSet import BaseBodyFilterSet

from ed_body.models import Star

class StarFilterSet(BaseBodyFilterSet):

    class Meta:
        model = Star
        fields = {
            'name': ['exact'],
            'system': ['exact'],
            'distance': ['lt', 'lte', 'gt', 'gte'],
            'luminosity': ['exact'],
            'starType': ['exact']
        }
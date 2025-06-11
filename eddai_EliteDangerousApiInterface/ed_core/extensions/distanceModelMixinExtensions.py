from django.utils.translation import gettext_lazy as _
from drf_spectacular.extensions import OpenApiViewExtension
from drf_spectacular.utils import OpenApiParameter, OpenApiTypes, extend_schema_view, extend_schema

from ed_core.api.mixins import DistanceModelMixin

class DistanceModelMixinExtensions(OpenApiViewExtension):
    target_class = DistanceModelMixin
    match_subclasses = True

    distance_parameters = [
        OpenApiParameter(
            name="distance_by_system",
            description=_('ID of the system from which to calculate the distance between systems'),
            type=OpenApiTypes.INT64,
            required=False,
        ),
        OpenApiParameter(
            name='order_distance_by_system',
            description=_('Order the results by distance from the specified system'),
            default='distance_st',
            type=OpenApiTypes.STR,
            enum=['distance_st', '-distance_st'],
            required=False,
        ),
        OpenApiParameter(
            name='filter_distance_by_system__lt',
            description=_('Filter systems with a distance less than the specified value (in Ly). '
                          'If no distance limit is provided, the system sets a maximum distance of 200 Ly.'),
            type=OpenApiTypes.FLOAT,
            required=False,
        ),
        OpenApiParameter(
            name='filter_distance_by_system__gt',
            description=_('Filter systems with a distance greater than the specified value (in Ly). '
                          'If no distance limit is provided, the system sets a maximum distance of 200 Ly.'),
            type=OpenApiTypes.FLOAT,
            required=False,
        ),
    ]

    def view_replacement(self):
        return extend_schema_view(
            list=extend_schema(
                parameters=self.distance_parameters
            )
        )(self.target)
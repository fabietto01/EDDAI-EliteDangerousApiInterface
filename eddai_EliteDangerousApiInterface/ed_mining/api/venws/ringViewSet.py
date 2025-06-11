from core.api.viewsets import OwnerAndDateModelViewSet
from ed_core.api.mixins import DistanceModelMixin
from django.utils.translation import gettext_lazy as _

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from ..filterset import RingFilterSet
from ..serializers import RingSerializer, RingDistanceSerializer

from ed_mining.models import Ring

from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes
)

@extend_schema_view(
    list=extend_schema(
        description=_("Returns a list of rings."),
        parameters=[
            OpenApiParameter(name='name',description=_("Filter rings by their name."),required=False,type=OpenApiTypes.STR),
            OpenApiParameter(name='body',description=_("Filter rings by the body ID they belong to."),required=False,type=OpenApiTypes.INT64),
            OpenApiParameter(name='body__system',description=_("Filter rings by the system ID of their parent body."),required=False,type=OpenApiTypes.INT64),
            OpenApiParameter(name='ringType',description=_("Filter rings by their exact ring type."),required=False,type=OpenApiTypes.STR),
            OpenApiParameter(name='ringType__in',description=_("Filter rings by a list of ring types (comma-separated)."),required=False,type=OpenApiTypes.STR),
        ]
    ),
    retrieve=extend_schema(description=_("Returns the details of a ring by its ID")),
    create=extend_schema(description=_("Creates a new ring object.")),
    update=extend_schema(description=_("Updates an existing ring object.")),
    partial_update=extend_schema(description=_("Partially updates an existing ring object.")),
    destroy=extend_schema(description=_("Deletes an existing ring object."))
)
class RingViewSet(DistanceModelMixin, OwnerAndDateModelViewSet):
    """
    RingViewSet is a view set for handling API requests related to Ring objects.
    Inherits from:
        OwnerAndDateModelViewSet: A custom view set that includes owner and date information.
    Attributes:
        queryset (QuerySet): A Django QuerySet that retrieves all Ring objects.
        serializer_class (Serializer
    """

    queryset = Ring.objects.all().order_by('id')
    serializer_class = RingSerializer
    distance_serializer_class = RingDistanceSerializer
    filter_param_distance = 'distance_by_system'
    filterset_class = RingFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']
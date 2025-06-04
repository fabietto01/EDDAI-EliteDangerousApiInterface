from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import ListModelMixin
from ed_core.api.mixins import DistanceModelMixin
from django.utils.translation import gettext_lazy as _

from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from ..filterSet import BaseBodyFilterSet
from ..serializers import BaseBodySerializer, BaseBodyDistanceSerializer

from ed_body.models import BaseBody

from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(
        description=_("Returns a list of celestial bodies, including both planets and stars."),
    ),
)
class BaseBodyViewSet(DistanceModelMixin, ListModelMixin, GenericViewSet):
    
    queryset = BaseBody.objects.all().select_related("star", "planet")
    serializer_class = BaseBodySerializer
    distance_serializer_class = BaseBodyDistanceSerializer
    filter_param_distance = 'distance_by_system'
    filterset_class = BaseBodyFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']

from rest_framework.viewsets import GenericViewSet, mixins
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes
)

from core.api.viewsets import OwnerAndDateModelViewSet
from ed_bgs.api.filterSet.powerInSystemFilterSet import PowerInSystemFilterSet
from ed_bgs.api.serializers import (
    PowerInSystemBasicInformationSerializer,
    PowerInSystemFromSystemSerializer,
    PowerInSystemSerializer,
)
from ed_bgs.models import PowerInSystem
from django.utils.translation import gettext_lazy as _


@extend_schema_view(
    list=extend_schema(description=_("Retrieve a list of all powers in systems.")),
    retrieve=extend_schema(description=_("Get detailed information about a specific power in system by its ID.")),
    create=extend_schema(description=_("Create a new power in system record.")),
    update=extend_schema(description=_("Update an existing power in system record.")),
    destroy=extend_schema(description=_("Delete a power in system record.")),
)
class PowerInSystemViewSet(OwnerAndDateModelViewSet):
    queryset = PowerInSystem.objects.select_related('system', 'power', 'state')
    serializer_class = PowerInSystemSerializer
    filterset_class = PowerInSystemFilterSet
    filter_backends = [DjangoFilterBackend]

    def get_serializer_class(self):
        """Use basic information serializer for list action, detail serializer for others."""
        if self.action == 'list':
            return PowerInSystemBasicInformationSerializer
        return super().get_serializer_class()


@extend_schema_view(
    list=extend_schema(
        description=_("Retrieve a list of powers in a specific system."),
        parameters=[OpenApiParameter(name='id', description=_("The ID of the system."), type=OpenApiTypes.INT, location=OpenApiParameter.PATH, required=True)],
    )
)
class PowerInSystemFromSystemViewSet(GenericViewSet, mixins.ListModelMixin):
    queryset = PowerInSystem.objects.select_related('power', 'state')
    serializer_class = PowerInSystemFromSystemSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(system_id=self.kwargs['id'])

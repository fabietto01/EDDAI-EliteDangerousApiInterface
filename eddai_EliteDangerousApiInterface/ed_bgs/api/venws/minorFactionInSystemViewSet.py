from http import HTTPMethod

from django.db.utils import IntegrityError
from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, mixins
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes
)

from core.api.viewsets import OwnerAndDateModelViewSet
from ed_bgs.api.filterSet.minorFactionInSystemFilterSet import MinorFactionInSystemFilterSet
from ed_bgs.api.serializers import (
    MinorFactionInSystemBasicInformationSerializer,
    MinorFactionInSystemFromsystemSerializer,
    MinorFactionInSystemSerializer,
    StateInMinorFactionSerializer,
)
from ed_bgs.models import MinorFactionInSystem

@extend_schema_view(
    list=extend_schema(description=_("Retrieve a list of all minor factions in systems.")),
    retrieve=extend_schema(description=_("Get detailed information about a specific minor faction in system by its ID.")),
    create=extend_schema(description=_("Create a new minor faction in system record.")),
    update=extend_schema(description=_("Update an existing minor faction in system record.")),
    destroy=extend_schema(description=_("Delete a minor faction in system record.")),
)
class MinorFactionInSystemViewSet(OwnerAndDateModelViewSet):
    queryset = MinorFactionInSystem.objects.select_related('system', 'minorFaction').prefetch_related('ed_bgs_stateinminorfaction_related')
    serializer_class = MinorFactionInSystemSerializer
    filterset_class = MinorFactionInSystemFilterSet
    filter_backends = [DjangoFilterBackend]

    def get_serializer_class(self):
        """Use basic information serializer for list action, detail serializer for others."""
        if self.action == 'list':
            return MinorFactionInSystemBasicInformationSerializer
        return super().get_serializer_class()        

@extend_schema_view(
    list=extend_schema(
        description=_("Retrieve a list of minor factions in a specific system."),
        parameters=[OpenApiParameter(name='system_pk', description=_("The ID of the system."), type=OpenApiTypes.INT, location=OpenApiParameter.PATH, required=True)],
    )
)
class MinorFactionInSystemFromSystemSerializer(GenericViewSet, mixins.ListModelMixin):
    queryset = MinorFactionInSystem.objects.select_related('minorFaction').prefetch_related('ed_bgs_stateinminorfaction_related')
    serializer_class = MinorFactionInSystemFromsystemSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(system_id=self.kwargs['id'])

from rest_framework.filters import SearchFilter
from core.api.viewsets import OwnerAndDateModelViewSet
from ed_bgs.api.serializers import PowerInSystemSerializer
from ed_bgs.models import PowerInSystem
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes

@extend_schema_view(
    list=extend_schema(
        description=_("Retrieve a list of powers in a specific system."),
        parameters=[OpenApiParameter(name='system_pk', description=_("The ID of the system."), type=OpenApiTypes.INT, location=OpenApiParameter.PATH, required=True)],
    ),
    retrieve=extend_schema(
        description=_("Get detailed information about a specific power in a system."),
        parameters=[OpenApiParameter(name='system_pk', description=_("The ID of the system."), type=OpenApiTypes.INT, location=OpenApiParameter.PATH, required=True)],
    ),
    create=extend_schema(
        description=_("Add a power to a system."),
        parameters=[OpenApiParameter(name='system_pk', description=_("The ID of the system."), type=OpenApiTypes.INT, location=OpenApiParameter.PATH, required=True)],
    ),
    update=extend_schema(
        description=_("Update a power in a system."),
        parameters=[OpenApiParameter(name='system_pk', description=_("The ID of the system."), type=OpenApiTypes.INT, location=OpenApiParameter.PATH, required=True)],
    ),
    destroy=extend_schema(
        description=_("Remove a power from a system."),
        parameters=[OpenApiParameter(name='system_pk', description=_("The ID of the system."), type=OpenApiTypes.INT, location=OpenApiParameter.PATH, required=True)],
    ),
)
class PowerInSystemViewSet(OwnerAndDateModelViewSet):
    queryset = PowerInSystem.objects.select_related('system', 'power', 'state', 'created_by', 'updated_by')
    serializer_class = PowerInSystemSerializer
    filter_backends = [SearchFilter]
    search_fields = ['power__name']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(system=self.kwargs['system_pk'])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'system_pk': self.kwargs['system_pk']})
        return context

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(system_id=self.kwargs['system_pk'], created_by=user, updated_by=user)

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(system_id=self.kwargs['system_pk'], updated_by=user)

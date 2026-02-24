from rest_framework.filters import SearchFilter
from core.api.viewsets import OwnerAndDateModelViewSet
from ed_bgs.api.serializers import StateInMinorFactionSerializer
from ed_bgs.models import StateInMinorFaction
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes

@extend_schema_view(
    list=extend_schema(
        description=_("Retrieve a list of states for a specific minor faction in a system."),
        parameters=[OpenApiParameter(name='minorfactioninsystem_pk', description=_("The ID of the minor faction in system."), type=OpenApiTypes.INT, location=OpenApiParameter.PATH, required=True)],
    ),
    retrieve=extend_schema(
        description=_("Get detailed information about a specific state of a minor faction in a system."),
        parameters=[OpenApiParameter(name='minorfactioninsystem_pk', description=_("The ID of the minor faction in system."), type=OpenApiTypes.INT, location=OpenApiParameter.PATH, required=True)],
    ),
    create=extend_schema(
        description=_("Add a state to a minor faction in a system."),
        parameters=[OpenApiParameter(name='minorfactioninsystem_pk', description=_("The ID of the minor faction in system."), type=OpenApiTypes.INT, location=OpenApiParameter.PATH, required=True)],
    ),
    update=extend_schema(
        description=_("Update a state of a minor faction in a system."),
        parameters=[OpenApiParameter(name='minorfactioninsystem_pk', description=_("The ID of the minor faction in system."), type=OpenApiTypes.INT, location=OpenApiParameter.PATH, required=True)],
    ),
    destroy=extend_schema(
        description=_("Remove a state from a minor faction in a system."),
        parameters=[OpenApiParameter(name='minorfactioninsystem_pk', description=_("The ID of the minor faction in system."), type=OpenApiTypes.INT, location=OpenApiParameter.PATH, required=True)],
    ),
)
class StateInMinorFactionViewSet(OwnerAndDateModelViewSet):
    queryset = StateInMinorFaction.objects.select_related('minorFaction', 'state', 'created_by', 'updated_by')
    serializer_class = StateInMinorFactionSerializer
    filter_backends = [SearchFilter]
    search_fields = ['state__name']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(minorFaction=self.kwargs['minorfactioninsystem_pk'])

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'minorfactioninsystem_pk': self.kwargs['minorfactioninsystem_pk']})
        return context

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(minorFaction_id=self.kwargs['minorfactioninsystem_pk'], created_by=user, updated_by=user)

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(minorFaction_id=self.kwargs['minorfactioninsystem_pk'], updated_by=user)

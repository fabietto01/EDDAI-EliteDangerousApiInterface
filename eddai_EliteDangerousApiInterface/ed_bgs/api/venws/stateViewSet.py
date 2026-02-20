from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter
from ed_bgs.api.serializers import StateSerializer, StateBasicInformationSerializer
from ed_bgs.models import State
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(description=_("Retrieve a list of all states available in the game.")),
    retrieve=extend_schema(description=_("Get detailed information about a specific state by its ID.")),
)
class StateViewSet(ReadOnlyModelViewSet):
    queryset = State.objects.all()
    serializer_class = StateSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return StateBasicInformationSerializer
        return super().get_serializer_class()

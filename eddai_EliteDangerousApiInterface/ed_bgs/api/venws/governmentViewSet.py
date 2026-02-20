from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter
from ed_bgs.api.serializers import GovernmentSerializer, GovernmentBasicInformationSerializer
from ed_bgs.models import Government
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(description=_("Retrieve a list of all governments available in the game.")),
    retrieve=extend_schema(description=_("Get detailed information about a specific government by its ID.")),
)
class GovernmentViewSet(ReadOnlyModelViewSet):
    queryset = Government.objects.all()
    serializer_class = GovernmentSerializer
    filter_backends = [SearchFilter]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return GovernmentBasicInformationSerializer
        return super().get_serializer_class()

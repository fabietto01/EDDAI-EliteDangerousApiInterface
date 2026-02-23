from http import HTTPMethod
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.db.utils import IntegrityError


from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from ed_bgs.api.filterSet.minorFactionFilterSet import MinorFactionFilterSet
from core.api.viewsets import OwnerAndDateModelViewSet
from ed_bgs.api.serializers import (
    MinorFactionSerializer, MinorFactionBasicInformation, 
    MinorFactionInSystemFromMinorFactionSerializer
)
from ed_bgs.models import MinorFaction, MinorFactionInSystem
from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes
)

@extend_schema_view(
    list=extend_schema(description=_("Retrieve a list of all minor factions.")),
    retrieve=extend_schema(description=_("Get detailed information about a specific minor faction by its ID.")),
    create=extend_schema(description=_("Create a new minor faction.")),
    update=extend_schema(description=_("Update an existing minor faction.")),
    destroy=extend_schema(description=_("Delete a minor faction.")),
)
class MinorFactionViewSet(OwnerAndDateModelViewSet):
    queryset = MinorFaction.objects.select_related('allegiance', 'government')
    serializer_class = MinorFactionSerializer
    filterset_class = MinorFactionFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return MinorFactionBasicInformation
        return super().get_serializer_class()
    
    @extend_schema(
        description=_("Retrieve a list of systems where the specified minor faction is present."),
        responses={200: MinorFactionInSystemFromMinorFactionSerializer(many=True)},
        filters=False,
    )
    @action(
        detail=True, 
        methods=[HTTPMethod.GET], 
        url_path='systems',
        url_name='systems'
    )
    def get_systems(self, request, pk=None):
        """
        Retrieve a list of systems where the specified minor faction is present.
        """
        try:
            minor_faction = self.get_object()
            if not minor_faction:
                return Response({'detail': _('Minor faction not found.')}, status=status.HTTP_404_NOT_FOUND)
            systems = MinorFactionInSystem.objects.filter(minorFaction=minor_faction).select_related('system').prefetch_related('ed_bgs_stateinminorfaction_related')
            page = self.paginate_queryset(systems)
            if page is not None:
                serializer = MinorFactionInSystemFromMinorFactionSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = MinorFactionInSystemFromMinorFactionSerializer(systems, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except IntegrityError:
            return Response({'detail': _('An error occurred while retrieving systems for the minor faction.')}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

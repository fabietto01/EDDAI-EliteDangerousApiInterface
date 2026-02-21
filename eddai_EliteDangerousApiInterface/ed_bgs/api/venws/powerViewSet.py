from http import HTTPMethod

from django.utils.translation import gettext_lazy as _

from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, extend_schema_view

from ed_bgs.api.filterSet.powerFilterSet import PowerFilterSet
from ed_bgs.api.serializers import (
    PowerSerializer,
    PowerBasicInformationSerializer,
    PowerInSystemFromSystemSerializer,
)
from ed_bgs.models import Power, PowerInSystem


@extend_schema_view(
    list=extend_schema(description=_("Retrieve a list of all powers available in the game.")),
    retrieve=extend_schema(description=_("Get detailed information about a specific power by its ID.")),
)
class PowerViewSet(ReadOnlyModelViewSet):
    queryset = Power.objects.select_related('headquarter', 'allegiance')
    serializer_class = PowerSerializer
    filterset_class = PowerFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']

    def get_serializer_class(self):
        if self.action == 'list':
            return PowerBasicInformationSerializer
        return super().get_serializer_class()

    @extend_schema(
        description=_("Retrieve a list of systems where the specified power is present."),
        responses={200: PowerInSystemFromSystemSerializer(many=True)},
        filters=False,
    )
    @action(
        detail=True,
        methods=[HTTPMethod.GET],
        url_path='systems'
    )
    def get_systems(self, request, pk=None):
        """
        Retrieve a list of systems where the specified power is present.
        """
        power = self.get_object()
        if not power:
            return Response({'detail': _('Power not found.')}, status=status.HTTP_404_NOT_FOUND)
        
        systems = PowerInSystem.objects.filter(power=power).select_related('system', 'state')
        
        # Apply pagination
        page = self.paginate_queryset(systems)
        if page is not None:
            serializer = PowerInSystemFromSystemSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = PowerInSystemFromSystemSerializer(systems, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

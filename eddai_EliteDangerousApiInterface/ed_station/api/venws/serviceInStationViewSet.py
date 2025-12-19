from core.api.viewsets import OwnerAndDateModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.serializers import ModelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _

from http import HTTPMethod
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from ..serializers import ServiceInStationSerializer
from ed_station.models import ServiceInStation, Station

from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes
)

@extend_schema_view(
    list=extend_schema(
        description=_("Returns a list of services available in a specific station."),
        parameters=[
            OpenApiParameter(name='station_pk', description=_("The primary key of the station to filter services."), location=OpenApiParameter.PATH, required=True, type=OpenApiTypes.INT64),
        ]
    ),
    retrieve=extend_schema(
        description=_("Returns the details of a specific service in a station by ID."),
        parameters=[
            OpenApiParameter(name='station_pk', description=_("The primary key of the station to filter services."), location=OpenApiParameter.PATH, required=True, type=OpenApiTypes.INT64),
        ]
    ),
    create=extend_schema(
        description=_("Creates a new service in a specific station."),
        parameters=[
            OpenApiParameter(name='station_pk', description=_("The primary key of the station where the service will be added."), location=OpenApiParameter.PATH, required=True, type=OpenApiTypes.INT64),
        ]
    ),
    update=extend_schema(
        description=_("Updates an existing service in a specific station."),
        parameters=[
            OpenApiParameter(name='station_pk', description=_("The primary key of the station where the service belongs."), location=OpenApiParameter.PATH, required=True, type=OpenApiTypes.INT64),
        ]
    ),
    partial_update=extend_schema(
        description=_("Partially updates an existing service in a specific station."),
        parameters=[
            OpenApiParameter(name='station_pk', description=_("The primary key of the station where the service belongs."), location=OpenApiParameter.PATH, required=True, type=OpenApiTypes.INT64),
        ]
    ),
    destroy=extend_schema(
        description=_("Deletes an existing service in a specific station."),
        parameters=[
            OpenApiParameter(name='station_pk', description=_("The primary key of the station where the service belongs."), location=OpenApiParameter.PATH, required=True, type=OpenApiTypes.INT64),
        ]
    )
)
class ServiceInStationViewSet(OwnerAndDateModelViewSet):

    """
    ServiceInStationViewSet is a view set for handling API requests related to ServiceInStation objects.
    """
    
    queryset = ServiceInStation.objects.select_related(
        'service',
        'station',
        'created_by',
        'updated_by'
    )
    serializer_class = ServiceInStationSerializer
    filterset_class = None
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['service__name']

    def get_queryset(self):
        """
        Returns a queryset of ServiceInStation objects filtered by station ID.
        """
        queryset = super().get_queryset()
        return queryset.filter(station=self.kwargs['station_pk'])
    
    def get_serializer_context(self):
        """
        Returns the serializer context with the station ID.
        """
        context = super().get_serializer_context()
        context.update({
            'station_pk': self.kwargs['station_pk']
        })
        return context
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(
            station_id=self.kwargs["station_pk"],
            created_by=user,
            updated_by=user
        )

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(
            station_id=self.kwargs['station_pk'],
            updated_by=user
        )

    @extend_schema(
        description=_("Bulk adds multiple services to a specific station."),
        parameters=[
            OpenApiParameter(name='station_pk', description=_("The primary key of the station where the services will be added."), location=OpenApiParameter.PATH, required=True, type=OpenApiTypes.INT64),
        ],
        request=ServiceInStationSerializer(many=True),
        responses={201: ServiceInStationSerializer(many=True)}
    )
    @action(
        detail=False,
        methods=[HTTPMethod.POST],
        url_name="multiple-adds",
        url_path="adds",
    )
    def multiple_add_service(self, request, station_pk=None, pk=None) -> None:
        if Station.objects.filter(pk=station_pk).exists():
            try:
                serializer:ModelSerializer = self.get_serializer(
                    data=request.data,
                    many=True
                )
                if serializer.is_valid():
                    user = self.request.user
                    serializer.save(
                        created_by=user,
                        updated_by=user,
                        station_id=self.kwargs['station_pk']
                    )
                    return Response(
                        serializer.data,
                        status=status.HTTP_201_CREATED
                    )
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            except Exception:
                return Response(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return  Response(
            {'detail': _('Station not found')},
            status=status.HTTP_404_NOT_FOUND
        )
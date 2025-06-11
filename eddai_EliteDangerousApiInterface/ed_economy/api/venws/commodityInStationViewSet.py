from core.api.viewsets import OwnerAndDateModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.serializers import ModelSerializer
from django_filters.rest_framework import DjangoFilterBackend

from http import HTTPMethod
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from ed_economy.api.serializers import CommodityInStationSerializer
from ed_economy.models import CommodityInStation
from ed_station.models import Station

from django.utils.translation import gettext_lazy as _
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes

@extend_schema_view(
    list=extend_schema(
        description=_("Retrieve a list of commodities available in a specific station."),
        parameters=[
            OpenApiParameter(name='station_pk', description=_("The ID of the station to filter commodities by."), type=OpenApiTypes.INT, location=OpenApiParameter.PATH, required=True),
        ],
    ),
    retrieve=extend_schema(
        description=_("Get detailed information about a specific commodity in a station by its ID."),
        parameters=[
            OpenApiParameter(name='station_pk', description=_("The ID of the station to filter commodities by."), type=OpenApiTypes.INT, location=OpenApiParameter.PATH, required=True),
        ],
    ),
    create=extend_schema(
        description=_("Add a new commodity to a specific station."),
        parameters=[
            OpenApiParameter(name='station_pk', description=_("The ID of the station to filter commodities by."), type=OpenApiTypes.INT, location=OpenApiParameter.PATH, required=True),
        ],
    ),
    update=extend_schema(
        description=_("Update an existing commodity in a specific station."),
        parameters=[
            OpenApiParameter(name='station_pk', description=_("The ID of the station to filter commodities by."), type=OpenApiTypes.INT, location=OpenApiParameter.PATH, required=True),
        ],
    ),
    destroy=extend_schema(
        description=_("Delete a commodity from a specific station."),
        parameters=[
            OpenApiParameter(name='station_pk', description=_("The ID of the station to filter commodities by."), type=OpenApiTypes.INT, location=OpenApiParameter.PATH, required=True),
        ],
    ),
)
class CommodityInStationViewSet(OwnerAndDateModelViewSet):
    """
    CommodityInStationViewSet is a view set for handling API requests related to CommodityInStation objects.
    """
    
    queryset = CommodityInStation.objects.all()
    serializer_class = CommodityInStationSerializer
    filterset_class = None
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['commodity__name']

    def get_queryset(self):
        """
        Returns a queryset of CommodityInStation objects filtered by station ID.
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
        description=_("Allows adding multiple commodities in a single operation within the station."),
        parameters=[
            OpenApiParameter(name='station_pk', description=_("The ID of the station to filter commodities by."), type=OpenApiTypes.INT, location=OpenApiParameter.PATH, required=True),
        ],
        request=CommodityInStationSerializer(many=True),
        responses={201: CommodityInStationSerializer(many=True)},
    )
    @action(
        detail=False,
        methods=[HTTPMethod.GET],
        url_name="multiple-adds",
        url_path="adds",
    )
    def multiple_add_commodities(self, request, station_pk=None, pk=None) -> None:
        """
        Add multiple commodities to a station.
        """
        if Station.objects.filter(pk=station_pk).exists():
            try:
                serializer:ModelSerializer = self.get_serializer(
                    data=request.data,
                    many=True,
                )
                if serializer.is_valid():
                    user = self.request.user
                    serializer.save(
                        station_id=self.kwargs['station_pk'],
                        created_by=user,
                        updated_by=user
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
        return Response(
            {'detail': _('the specified station does not exist.'),},
            status=status.HTTP_404_NOT_FOUND
        )
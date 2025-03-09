from core.api.viewsets import OwnerAndDateModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.serializers import ModelSerializer
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _

from http import HTTPMethod
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.db.utils import IntegrityError

from ed_body.models import AtmosphereComponentInPlanet, Planet

from ..serializers import AtmosphereComponentInPlanetSerializer


from drf_spectacular.utils import extend_schema, extend_schema_view

@extend_schema_view(
    list=extend_schema(
        description="Returns a list of atmosphere components in a planet",
    ),
    retrieve=extend_schema(description="Returns the details of an atmosphere component in a planet by ID"),
)
class AtmosphereComponentInPlanetViewSet(OwnerAndDateModelViewSet):
    """
    AtmosphereComponentInPlanetViewSet is a view set for handling API requests related to AtmosphereComponentInPlanet objects.
    """

    queryset = AtmosphereComponentInPlanet.objects.all()
    serializer_class = AtmosphereComponentInPlanetSerializer
    filterset_class = None
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['atmosphere_component__name']

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(planet=self.kwargs['planet_pk'])
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({
            'planet_pk': self.kwargs['planet_pk']
        })
        return context
        
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(
            planet_id=self.kwargs['planet_pk'],
            created_by=user,
            updated_by=user
        )

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(
            planet_id=self.kwargs['planet_pk'],
            updated_by=user
        )

    @extend_schema(
        description="Adds an atmosphere component to a planet",
        request=AtmosphereComponentInPlanetSerializer(many=True),
        responses={201: AtmosphereComponentInPlanetSerializer(many=True)}
    )
    @action(
        detail=False,
        methods=[HTTPMethod.POST],
        url_name="multiple-add",
        url_path="add"
    )
    def multiple_add_atmosphere_components(self, request, planet_pk=None, pk=None) -> None:
        """
        Adds multiple atmosphere components to a planet.

        This method handles the addition of multiple atmosphere components to a specified planet.
        It validates the incoming data using a serializer and saves the components if valid.
        If the components already exist, it returns a 400 Bad Request response.
        If any other error occurs, it returns a 500 Internal Server Error response.
        If the queryset does not exist, it returns a 404 Not Found response.

        Args:
            request (Request): The HTTP request object containing the data to be added.
            planet_pk (int, optional): The primary key of the planet to which the components are to be added. Defaults to None.
            pk (int, optional): The primary key of the atmosphere component. Defaults to None.

        Returns:
            Response: A DRF Response object with the appropriate status code and data.
        """
        if Planet.objects.filter(pk=planet_pk).exists():
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
                        planet_id=self.kwargs['planet_pk']
                    )
                    return Response(
                        serializer.data,
                        status=status.HTTP_201_CREATED
                    )
                return Response(
                    serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST
                )
            except IntegrityError as e:
                if 'planet_atmo_component_uc' in str(e):
                    return Response(
                        {'detail': _('One or more atmosphere components already exist for this planet.')},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            except Exception:
                return Response(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
        return  Response(
            {'detail': _('The specified planet does not exist.')},
            status=status.HTTP_404_NOT_FOUND
        )
    
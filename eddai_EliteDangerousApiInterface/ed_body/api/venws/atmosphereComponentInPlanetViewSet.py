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

from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes
)

@extend_schema_view(
    list=extend_schema(
        description=_("Returns a list of atmosphere components in a planet"),
        parameters=[
            OpenApiParameter(name='planet_pk', description=_("The primary key of the planet to filter atmosphere components."), location=OpenApiParameter.PATH, required=True, type=OpenApiTypes.INT64),
        ]
    ),
    retrieve=extend_schema(
        description=_("Returns the details of an atmosphere component in a planet by ID"),
        parameters=[
            OpenApiParameter(name='planet_pk', description=_("The primary key of the planet to filter atmosphere components."), location=OpenApiParameter.PATH, required=True, type=OpenApiTypes.INT64),
        ]
    ),
    create=extend_schema(
        description=_("Creates a new atmosphere component in a planet"),
        parameters=[
            OpenApiParameter(name='planet_pk', description=_("The primary key of the planet to which the atmosphere component will be added."), location=OpenApiParameter.PATH, required=True, type=OpenApiTypes.INT64),
        ]
    ),
    update=extend_schema(
        description=_("Updates an existing atmosphere component in a planet"),
        parameters=[
            OpenApiParameter(name='planet_pk', description=_("The primary key of the planet to which the atmosphere component belongs."), location=OpenApiParameter.PATH, required=True, type=OpenApiTypes.INT64),
        ]
    ),
    partial_update=extend_schema(
        description=_("Partially updates an existing atmosphere component in a planet"),
        parameters=[
            OpenApiParameter(name='planet_pk', description=_("The primary key of the planet to which the atmosphere component belongs."), location=OpenApiParameter.PATH, required=True, type=OpenApiTypes.INT64),
        ]
    ),
    destroy=extend_schema(
        description=_("Deletes an existing atmosphere component in a planet"),
        parameters=[
            OpenApiParameter(name='planet_pk', description=_("The primary key of the planet to which the atmosphere component belongs."), location=OpenApiParameter.PATH, required=True, type=OpenApiTypes.INT64),
        ]   
    )
)
class AtmosphereComponentInPlanetViewSet(OwnerAndDateModelViewSet):
    """
    ViewSet for managing atmosphere components associated with a specific planet.
    This ViewSet provides CRUD operations for `AtmosphereComponentInPlanet` objects, scoped to a given planet via the `planet_pk` URL parameter. It supports searching by atmosphere component name and allows bulk creation of atmosphere components for a planet through a custom action.
    Key Features:
    - Restricts queryset to atmosphere components belonging to the specified planet.
    - Passes `planet_pk` in the serializer context for contextual validation or processing.
    - Automatically sets `created_by` and `updated_by` fields on creation and update.
    - Provides a `multiple_add_atmosphere_components` action to add multiple atmosphere components to a planet in a single request, with appropriate error handling for duplicates and missing planets.
    Attributes:
        queryset: Queryset of all AtmosphereComponentInPlanet objects.
        serializer_class: Serializer for AtmosphereComponentInPlanet.
        filterset_class: Disabled (set to None).
        filter_backends: Enables search and Django filter backends.
        search_fields: Allows searching by the name of the atmosphere component.
    Custom Actions:
        multiple_add_atmosphere_components: Bulk add endpoint for atmosphere components, with validation and error responses for duplicates or missing planets.
    """

    queryset = AtmosphereComponentInPlanet.objects.select_related(
        'atmosphere_component',
        'planet',
        'created_by',
        'updated_by'
    )
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
        description=_("Allows adding multiple atmospheric components in a single operation for a planet."),
        parameters=[
            OpenApiParameter(name='planet_pk', description=_("The primary key of the planet to which the atmosphere components will be added."), location=OpenApiParameter.PATH, required=True, type=OpenApiTypes.INT64),
        ],
        request=AtmosphereComponentInPlanetSerializer(many=True),
        responses={201: AtmosphereComponentInPlanetSerializer(many=True)}
    )
    @action(
        detail=False,
        methods=[HTTPMethod.POST],
        url_name="multiple-adds",
        url_path="adds",
    )
    def multiple_add_atmosphere_components(self, request, planet_pk=None, pk=None) -> None:
        """
        Adds multiple atmosphere components to a specified planet.
        This method accepts a list of atmosphere component data in the request body and attempts to create them for the planet identified by `planet_pk`. 
        If the planet does not exist, a 404 response is returned. If any of the components already exist for the planet (based on a unique constraint), 
        a 400 response is returned with a relevant error message. On successful creation, returns the serialized data with a 201 status code. 
        Handles validation errors and unexpected exceptions with appropriate HTTP responses.
        Args:
            request (Request): The HTTP request object containing the data to be added.
            planet_pk (int, optional): The primary key of the planet to which components are to be added.
            pk (int, optional): The primary key of the resource (not used in this method).
        Returns:
            Response: A DRF Response object with the result of the operation.
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
    
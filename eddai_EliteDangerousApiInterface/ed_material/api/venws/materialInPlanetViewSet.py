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

from ed_material.models import MaterialInPlanet
from ed_body.models import Planet

from ..serializers import MaterialInPlanetSerializer

from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes
)

@extend_schema_view(
    list=extend_schema(
        description=_("Returns a list of materials in a planet"),
        parameters=[
            OpenApiParameter(name='planet_pk', description=_("The primary key of the planet to filter materials."), location=OpenApiParameter.PATH, required=True, type=OpenApiTypes.INT64),
        ]
    ),
    retrieve=extend_schema(
        description=_("Returns the details of a material in a planet by ID"),
        parameters=[
            OpenApiParameter(name='planet_pk', description=_("The primary key of the planet to filter materials."), location=OpenApiParameter.PATH, required=True, type=OpenApiTypes.INT64),
        ]
    ),
    create=extend_schema(
        description=_("Creates a new material in a planet"),
        parameters=[
            OpenApiParameter(name='planet_pk', description=_("The primary key of the planet to which the material will be added."), location=OpenApiParameter.PATH, required=True, type=OpenApiTypes.INT64),
        ]
    ),
    update=extend_schema(
        description=_("Updates an existing material in a planet"),
        parameters=[
            OpenApiParameter(name='planet_pk', description=_("The primary key of the planet to which the material belongs."), location=OpenApiParameter.PATH, required=True, type=OpenApiTypes.INT64),
        ]
    ),
    partial_update=extend_schema(
        description=_("Partially updates an existing material in a planet"),
        parameters=[
            OpenApiParameter(name='planet_pk', description=_("The primary key of the planet to which the material belongs."), location=OpenApiParameter.PATH, required=True, type=OpenApiTypes.INT64),
        ]
    ),
    destroy=extend_schema(
        description=_("Deletes an existing material in a planet"),
        parameters=[
            OpenApiParameter(name='planet_pk', description=_("The primary key of the planet to which the material belongs."), location=OpenApiParameter.PATH, required=True, type=OpenApiTypes.INT64),
        ]   
    )
)
class MaterialInPlanetViewSet(OwnerAndDateModelViewSet):
    """
    ViewSet for managing materials associated with a specific planet.
    This ViewSet provides CRUD operations for `MaterialInPlanet` objects, scoped to a given planet via the `planet_pk` URL parameter. It supports searching by material name and allows bulk creation of materials for a planet through a custom action.
    Key Features:
    - Restricts queryset to materials belonging to the specified planet.
    - Passes `planet_pk` in the serializer context for contextual validation or processing.
    - Automatically sets `created_by` and `updated_by` fields on creation and update.
    - Provides a `multiple_add_materials` action to add multiple materials to a planet in a single request, with appropriate error handling for duplicates and missing planets.
    Attributes:
        queryset: Queryset of all MaterialInPlanet objects.
        serializer_class: Serializer for MaterialInPlanet.
        filterset_class: Disabled (set to None).
        filter_backends: Enables search and Django filter backends.
        search_fields: Allows searching by the name of the material.
    Custom Actions:
        multiple_add_materials: Bulk add endpoint for materials, with validation and error responses for duplicates or missing planets.
    """

    queryset = MaterialInPlanet.objects.all()
    serializer_class = MaterialInPlanetSerializer
    filterset_class = None
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['material__name']

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
        description=_("Allows adding multiple materials in a single operation for a planet."),
        parameters=[
            OpenApiParameter(name='planet_pk', description=_("The primary key of the planet to which the materials will be added."), location=OpenApiParameter.PATH, required=True, type=OpenApiTypes.INT64),
        ],
        request=MaterialInPlanetSerializer(many=True),
        responses={201: MaterialInPlanetSerializer(many=True)}
    )
    @action(
        detail=False,
        methods=[HTTPMethod.POST],
        url_name="multiple-adds",
        url_path="adds",
    )
    def multiple_add_materials(self, request, planet_pk=None, pk=None) -> None:
        """
        Adds multiple materials to a specified planet.
        This method accepts a list of material data in the request body and attempts to create them for the planet identified by `planet_pk`. 
        If the planet does not exist, a 404 response is returned. If any of the materials already exist for the planet (based on a unique constraint), 
        a 400 response is returned with a relevant error message. On successful creation, returns the serialized data with a 201 status code. 
        Handles validation errors and unexpected exceptions with appropriate HTTP responses.
        Args:
            request (Request): The HTTP request object containing the data to be added.
            planet_pk (int, optional): The primary key of the planet to which materials are to be added.
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
                if 'planet_material_uc' in str(e):
                    return Response(
                        {'detail': _('One or more materials already exist for this planet.')},
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

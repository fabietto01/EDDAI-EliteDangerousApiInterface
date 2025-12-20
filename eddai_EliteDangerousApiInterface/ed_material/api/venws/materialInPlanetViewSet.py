from core.api.viewsets import OwnerAndDateModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.serializers import ModelSerializer
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.translation import gettext_lazy as _

from http import HTTPMethod
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.db.utils import IntegrityError

from ed_material.models import MaterialInPlanet
from ed_body.models import Planet
from ..filterSet import MaterialInPlanetFilterSet
from ..serializers import (
    CompactedMaterialInPlanetSerializer, 
    MaterialInPlanetSerializer
)

from drf_spectacular.utils import (
    extend_schema, extend_schema_view, OpenApiParameter, OpenApiTypes
)


@extend_schema_view(
    list=extend_schema(
        description=_("Retrieve a list of all materials present in a specific planet."),

    ),
    retrieve=extend_schema(
        description=_("Get detailed information about a specific material in a planet."),

    ),
    create=extend_schema(
        description=_("Add a new material to a planet with its percentage."),
        request=MaterialInPlanetSerializer,
    ),
    update=extend_schema(
        description=_("Update the percentage of a material in a planet."),
        request=MaterialInPlanetSerializer,
    ),
    partial_update=extend_schema(
        description=_("Partially update the percentage of a material in a planet."),
        request=MaterialInPlanetSerializer,
    ),
    destroy=extend_schema(
        description=_("Remove a material from a planet."),
    ),
)
class MaterialInPlanetViewSet(OwnerAndDateModelViewSet):

    queryset = MaterialInPlanet.objects.select_related('material', 'planet').all()
    serializer_class = MaterialInPlanetSerializer
    filterset_class = MaterialInPlanetFilterSet
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['material__name']

    def get_serializer_class(self):
        if self.action == 'list':
            return CompactedMaterialInPlanetSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        """
        Filtra i materiali per il pianeta specificato nell'URL
        """
        planet_pk = self.kwargs.get('planet_pk')
        if planet_pk:
            get_object_or_404(Planet, pk=planet_pk)
            return self.queryset.filter(planet_id=planet_pk)
        return self.queryset.none()

    def get_serializer_context(self):
        """
        Aggiungi planet_id al context del serializer
        """
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
        Create multiple materials associated with a specific planet.
        This method handles the creation of multiple material entries for a given planet.
        It validates the planet existence, processes the request data through a serializer,
        and handles various error cases including integrity constraint violations.
        Args:
            request: The HTTP request object containing the material data to be created.
            planet_pk (int, optional): The primary key of the planet to associate materials with.
            pk (int, optional): Additional primary key parameter (unused in this implementation).
        Returns:
            Response: HTTP response with one of the following:
                - 201 Created: Successfully created materials with serialized data
                - 400 Bad Request: Invalid data or materials already exist for the planet
                - 404 Not Found: Planet with given pk does not exist
                - 500 Internal Server Error: Unexpected error occurred
        Raises:
            IntegrityError: When trying to create duplicate materials for a planet
            Exception: For any other unexpected errors during processing
        Notes:
            - Automatically sets created_by and updated_by fields to the requesting user
            - Uses the planet_pk from URL kwargs to associate materials with the planet
            - Handles unique constraint violations specifically for planet-material relationships
        """
        
        if Planet.objects.filter(pk=planet_pk).exists():
            try:
                serializer:ModelSerializer = self.get_serializer(
                    data=request.data,
                    many=True,
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
                        {"detail": _("One or more materials already exist for this planet.")},
                        status=status.HTTP_400_BAD_REQUEST
                    )
                return Response(
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            except Exception:
                return Response(
                    {"detail": _("An unexpected error occurred.")},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                ) 
        return Response(
            {"detail": _("Planet not found.")},
            status=status.HTTP_404_NOT_FOUND
        )

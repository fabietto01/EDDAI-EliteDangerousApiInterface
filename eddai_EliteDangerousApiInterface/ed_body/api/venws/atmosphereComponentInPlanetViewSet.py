from core.api.viewsets import OwnerAndDateModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.serializers import ModelSerializer
from django_filters.rest_framework import DjangoFilterBackend

from http import HTTPMethod
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status
from django.db.utils import IntegrityError


from ed_body.models import AtmosphereComponentInPlanet

from ..serializers import AtmosphereComponentInPlanetSerializer

class AtmosphereComponentInPlanetViewSet(OwnerAndDateModelViewSet):
    """
    ViewSet for managing atmosphere components in a planet.
    This ViewSet provides CRUD operations for atmosphere components associated with a specific planet.
    It includes custom methods for adding multiple atmosphere components at once.
    Attributes:
        queryset (QuerySet): The queryset for retrieving atmosphere components.
        serializer_class (Serializer): The serializer class for atmosphere components.
        filterset_class (FilterSet): The filter set class for atmosphere components.
        filter_backends (list): The list of filter backends for the ViewSet.
        search_fields (list): The list of fields to search in the atmosphere components.
    Methods:
        get_queryset(self):
            Retrieves the queryset filtered by the specified planet.
        get_serializer_context(self):
            Adds the planet primary key to the serializer context.
        perform_create(self, serializer):
            Saves a new atmosphere component with the created_by and updated_by fields set to the current user.
        perform_update(self, serializer):
            Updates an existing atmosphere component with the updated_by field set to the current user.
        multiple_add_atmosphere_components(self, request, planet_pk=None, pk=None):
            Adds multiple atmosphere components to a specified planet.
            Validates the incoming data using a serializer and saves the components if valid.
            Returns appropriate responses based on the success or failure of the operation.
    """

    queryset = AtmosphereComponentInPlanet.objects.all()
    serializer_class = AtmosphereComponentInPlanetSerializer
    filterset_class = None
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['name']

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

    @action(
        detail=False,
        methods=[HTTPMethod.POST],
        url_name="atmosphere-component-multiple-add",
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
        queryset = self.get_queryset()
        if queryset.exists():
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
            status=status.HTTP_404_NOT_FOUND
        )
    
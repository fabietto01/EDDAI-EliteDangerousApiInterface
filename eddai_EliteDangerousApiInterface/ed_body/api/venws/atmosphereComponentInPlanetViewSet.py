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
    
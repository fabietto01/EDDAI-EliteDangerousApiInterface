from core.api.viewsets import OwnerAndDateModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.serializers import ModelSerializer
from django.utils.translation import gettext_lazy as _

from http import HTTPMethod
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

from ..serializers import HotSpotInRingSerializer
from ed_mining.models import HotSpot as HotSpotInRing, Ring

class HotSpotInRingViewSet(OwnerAndDateModelViewSet):
    """
    HotSpotInRingViewSet is a view set for handling API requests related to HotSpotInRing objects.
    """
    
    queryset = HotSpotInRing.objects.all()
    serializer_class = HotSpotInRingSerializer
    filter_backends = [SearchFilter]
    search_fields = ['type__name']

    def get_queryset(self):
        """
        Returns a queryset of HotSpotInRing objects filtered by ring ID.
        """
        queryset = super().get_queryset()
        return queryset.filter(ring=self.kwargs['ring_pk'])
    
    def get_serializer_context(self):
        """
        Returns the serializer context with the ring ID.
        """
        context = super().get_serializer_context()
        context.update({
            'ring_pk': self.kwargs['ring_pk']
        })
        return context
    
    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(
            ring_id=self.kwargs["ring_pk"],
            created_by=user,
            updated_by=user
        )

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(
            ring_id=self.kwargs['ring_pk'],
            updated_by=user
        )

    @action(
        detail=False,
        methods=[HTTPMethod.POST],
        url_path='multiple-adds',
        url_name='adds'
    )
    def multiple_adds(self, request, ring_pk, pk) -> None:
        if Ring.objects.filter(pk=ring_pk).exists():
            try:
                serializer:ModelSerializer = self.get_serializer(
                    data=request.data,
                    many=True
                )
                if serializer.is_valid():
                    serializer.save(
                        ring_id=ring_pk,
                        created_by=self.request.user,
                        updated_by=self.request.user
                    )
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response(
                    {
                        'error': str(e),
                        'message': _('An error occurred while processing your request.')
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        return Response(
            {'detail': _('Ring not found')},
            status=status.HTTP_404_NOT_FOUND
        )
from rest_framework import viewsets
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.decorators import action

from django.contrib.gis.db.models.functions import Distance
from core.Bechekd.Distance3D import Distance3D

from .serializers.SystemSerializer import SystemSerializer, SystemDistanceSerializer
from .filters import SystemFilterSet

from ed_system.models import System

class SystemViewSet(viewsets.ModelViewSet):
    """
    SystemViewSet is a viewset for handling System objects.
    Attributes:
        queryset (QuerySet): The queryset of System objects.
        serializer_class (Serializer): The serializer class for System objects.
        filterset_class (FilterSet): The filter set class for filtering System objects.
    Methods:
        from_system(request: Request, pk: int = None):
            Handles GET requests to retrieve systems ordered by their distance from a specified system.
            Annotates each system with its distance from the specified system and orders them by distance.
            Supports pagination if applicable.
            Args:
                request (Request): The HTTP request object.
                pk (int, optional): The primary key of the system. Defaults to None.
            Returns:
                Response: A paginated response or a list of serialized systems ordered by distance.
    """
    queryset = System.objects.all()
    serializer_class = SystemSerializer
    filterset_class = SystemFilterSet

    @action(
        detail=True, methods=['get'], serializer_class=SystemDistanceSerializer,
        url_path='from-system', url_name='from-system'
    )
    def from_system(self, request:Request, pk:int=None):
        system = self.get_object()
        qs = System.objects.annotate(distance=Distance3D('coordinate', system.coordinate)).order_by('distance')
        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)    
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)
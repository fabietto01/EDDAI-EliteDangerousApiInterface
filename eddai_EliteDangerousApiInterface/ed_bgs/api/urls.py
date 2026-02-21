from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .venws import (
    FactionViewSet,
    GovernmentViewSet,
    StateViewSet,
    PowerStateViewSet,
    PowerViewSet,
    MinorFactionViewSet,
    MinorFactionInSystemViewSet,
    MinorFactionInSystemFromSystemSerializer,
    StateInMinorFactionViewSet,
    PowerInSystemViewSet,
    PowerInSystemFromSystemViewSet,
)

router = DefaultRouter(trailing_slash=False)
router.register(r'bgs/factions', FactionViewSet)
router.register(r'bgs/governments', GovernmentViewSet)
router.register(r'bgs/states', StateViewSet)
router.register(r'bgs/power-states', PowerStateViewSet)
router.register(r'bgs/powers', PowerViewSet)
router.register(r'bgs/minor-factions', MinorFactionViewSet)
router.register(r'bgs/minor-factions-in-system', MinorFactionInSystemViewSet)
router.register(r'bgs/power-in-system', PowerInSystemViewSet)
router.register(r'bgs/minor-factions-in-system/(?P<minorfactioninsystem_pk>[^/.]+)/states', StateInMinorFactionViewSet)
router.register(r'system/(?P<id>[^/.]+)/minor-factions', MinorFactionInSystemFromSystemSerializer, basename='minor-factions-in-system-from-system')
router.register(r'system/(?P<id>[^/.]+)/powers', PowerInSystemFromSystemViewSet, basename='powers-in-system')

urlpatterns = router.urls

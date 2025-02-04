"""
URL configuration for eddai_EliteDangerousApiInterface project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .venws import (
    BaseBodyViewSet, StarViewSet, PlanetViewSet,
    AtmosphereComponentViewSet, AtmosphereComponentInPlanetViewSet,
    AtmosphereTypeViewSet, PlanetTypeViewSet, VolcanismViewSet,
    StarLuminosityViewSet, StarTypeViewSet
)

router = DefaultRouter(trailing_slash=False)
router.register(r'body', BaseBodyViewSet)
router.register(r'body/star', StarViewSet)
router.register(r'body/planet', PlanetViewSet)
router.register(r'body/planet/(?P<planet_pk>\d+)/atmosphere-component', AtmosphereComponentInPlanetViewSet)
router.register(r'atmosphere-component', AtmosphereComponentViewSet)
router.register(r'atmosphere-type', AtmosphereTypeViewSet)
router.register(r'planet-type', PlanetTypeViewSet)
router.register(r'volcanism', VolcanismViewSet)
router.register(r'star-luminosity', StarLuminosityViewSet)
router.register(r'star-type', StarTypeViewSet)

urlpatterns = router.urls
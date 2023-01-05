from django.http import HttpResponse
from django.db.models import Count, F, Value

from eddn.service.client import EddnClient

from ed_body.models import BaseBody

from ed_mining.models import HotspotSignals, HotSpot
from ed_body.models import BaseBody, Star, StarLuminosity, StarType, Planet
from ed_system.models import System 


# Create your views here.

def startEddn(request):
    cl = EddnClient()
    cl.start()
    return HttpResponse(status=400, reason='EDDN is not running')

def startTest(request):
    parent = BaseBody.objects.get(name='Test')

    Star.objects.create(
        name='Test',
        system=System.objects.get(name='sol'),
        bodyID=999999,
        absoluteMagnitude=6.0,
        age=6.0,
        luminosity=StarLuminosity.objects.get(name='Ia0'),
        starType=StarType.objects.get(name='O'),
        stellarMass=6.0,
        subclass=6,
    )
    Planet.objects.create(
        name='Test',
        system=System.objects.get(name='sol'),
        bodyID=999999,
        landable=True,
        massEM=999999,
    )

    return HttpResponse(status=200, reason='ok') 
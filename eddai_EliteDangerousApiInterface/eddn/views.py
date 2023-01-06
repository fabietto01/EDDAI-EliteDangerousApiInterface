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

    Planet.objects.create(
        name='Test1',
        system=System.objects.get(name='sol'),
        bodyID=999999,
        landable=True,
        massEM=999999,
    )

    return HttpResponse(status=200, reason='ok') 
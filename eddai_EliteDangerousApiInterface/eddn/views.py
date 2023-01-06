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

    return HttpResponse(status=200, reason='ok') 
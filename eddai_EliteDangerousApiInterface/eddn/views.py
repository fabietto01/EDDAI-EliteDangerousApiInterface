from django.http import HttpResponse
from django.db.models import Count, F, Value

from eddn.service import EddnClient

from ed_body.models import BaseBody

from ed_mining.models import HotspotSignals, HotSpot
from ed_body.models import BaseBody, Star, StarLuminosity, StarType, Planet
from ed_system.models import System 


from ed_system.tasks import test, add

# Create your views here.

def startEddn(request):
    cl = EddnClient()
    cl.run()
    return HttpResponse(status=400, reason='EDDN is not running')

def startTest(request):
    # instanze, crate = BaseBody.objects.get_or_create(
    #     defaults={
    #         'bodyID': 1,
    #         'distance': 1,
    #     },
    #     name='test', system=System.objects.get(name='test')
    # )
    # PlanetIStanze = Planet.objects.get_or_create(
    #     defaults={
    #         'bodyID': 999999,
    #     },
    #     name='Test', system=System.objects.get(name='Sol')
    # )
    t = test.delay()
    task = add.delay(1, 2)
    result = task.get()
    return HttpResponse(result,status=200, reason='ok') 
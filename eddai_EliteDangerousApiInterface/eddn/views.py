from django.http import HttpResponse
from django.shortcuts import render

from eddn.service.client import EddnClient

from ed_bgs.models import (
        Faction, Government, MinorFaction, 
        MinorFactionInSystem, State,
        StateInMinorFaction
    )

# Create your views here.

def startEddn(request):
    cl = EddnClient()
    cl.start()
    return HttpResponse(status=400, reason='EDDN is not running')

def startTest(request):
    
    StateInMinorFaction.objects.filter(phase="a").update(phase="A")
    
    return HttpResponse(status=200, reason='ok')
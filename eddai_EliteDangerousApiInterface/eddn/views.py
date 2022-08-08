from http.client import HTTPResponse
from django.shortcuts import render

from eddn.service.client import EddnClient

# Create your views here.


def startEddn(request):
    cl = EddnClient()
    cl.start()
    return HTTPResponse(status=400, reason='EDDN is not running')
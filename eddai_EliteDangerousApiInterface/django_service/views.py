from django.http import HttpResponse
from .services import test_service

from eddai_EliteDangerousApiInterface.celery import app

# Create your views here.


def manual_start(request):
    test_service.delay()
    return HttpResponse(status=200, reason='ok')


def test(request):

    p =  app.control.ping()
    r = app.control.inspect().registered()

    x = f"ping: {p},\n registered: {r}"

    return HttpResponse(x, status=200, reason='ok')
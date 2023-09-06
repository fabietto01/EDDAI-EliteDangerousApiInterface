from django.http import HttpResponse
from .services import test_service

# Create your views here.


def manual_start(request):
    test_service.delay()
    return HttpResponse(status=200, reason='ok')
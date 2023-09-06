from django.http import HttpResponse

from .tasks import add_eddn

# Create your views here.

# def startEddn(request):
#     cl = EddnClient()
#     cl.run()
#     return HttpResponse(status=400, reason='EDDN is not running')

def startTest(request):

    task = add_eddn.delay(1, 2)
    result = task.get()
    return HttpResponse(result,status=200, reason='ok') 
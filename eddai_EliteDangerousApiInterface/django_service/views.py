from django.http import HttpResponse, HttpResponseRedirect
from .services import test_service

from eddai_EliteDangerousApiInterface.celery import app

from celery.app.control import Control, Inspect
from celery.result import AsyncResult

# Create your views here.


def manual_start(request):
    test_service.delay()
    return HttpResponseRedirect("/services/test/")


def test(request):

    controle:Control = app.control

    dic = {}

    dic.update({"ping": controle.ping()})

    i:Inspect = controle.inspect()

    dic.update({"active": i.active()})
    dic.update({"registered": i.registered()})
    
    infoTask = []
    if type(dic.get('active', None)) is dict:
        for k, v in dic.get('active').items():
            for task in v:
                task_id = task.get('id')
                infoTask.append(
                    AsyncResult(task_id, app=app).status
                )
    dic.update({"informazioni sul tasci in corsa": infoTask})

    html = '<a href="/services/start/">start</a><br>'
    for k, v in dic.items():
        html += f"<br>{k}: {v}<br>"
    return HttpResponse(html, status=200, reason='ok')
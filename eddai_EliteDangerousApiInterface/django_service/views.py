from django.http import HttpResponse, HttpResponseRedirect
from .services import test_service, _TestService

#from eddai_EliteDangerousApiInterface.celery import app

from django_service.celey.utility import get_app, get_servis_list

from celery.app.control import Control, Inspect
from celery.result import AsyncResult

# Create your views here.

app = get_app()

def manual_start(request):
    _TestService().delay()
    return HttpResponseRedirect("/services/test/")


def manual_stop(request, id_task):
    app.control.revoke(id_task, terminate=True)
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

    dic.update({"tasck": get_servis_list(app)})

    html = '<a href="/services/start/">start</a><br>'
    html += '<a href="/services/stop/">stop</a><br>'
    for k, v in dic.items():
        html += f"<br>{k}: {v}<br>"
    return HttpResponse(html, status=200, reason='ok')
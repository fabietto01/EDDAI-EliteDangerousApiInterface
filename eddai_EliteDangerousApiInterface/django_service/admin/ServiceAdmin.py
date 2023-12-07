from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from django.db.models import QuerySet

from .ReadOnlyServiceEventInline import ReadOnlyServiceEventInline
from ..celey.utility import get_app, get_control

from celery.result import AsyncResult

from ..models import Service
from ..form import ServiceForm

app = get_app()

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'service',
        'status',
        'args',
        'kwargs',
        'routing_key'
    )
    list_filter = (
        'status',
        'routing_key'
    )
    search_fields = (
        'name',
        'status',
        'routing_key'
    )
    inlines = [ReadOnlyServiceEventInline]
    form = ServiceForm
    actions = [
        'start_service',
        'stop_service'
    ]

    @admin.action(description=_('start service'))
    def start_service(self, request, queryset:QuerySet[Service]):
        """
        Quista funzione permette di avviare un servizio,
        dal panello di aministrazioine di django.
        """
        for service in queryset:
            if service.status == service.Status.STOP:
                tasck:AsyncResult = app.send_task(
                    task_id=str(service.id),
                    name=service.service,
                    args=service.args,
                    kwargs=service.kwargs,
                    #routing_key=service.routing_key
                )
                service.status = Service.Status.RUN
                service.save()
                self.message_user(
                    request,
                    _('service %(service)s started with id %(id)s') % {
                        'service': service.name,
                        'id': tasck.service
                    },
                    messages.SUCCESS
                )
            else:
                self.message_user(
                    request,
                    _('service %(service)s Already in state %(state)s ') % {
                        'service': service.name,
                        'state': service.status
                    },
                    messages.WARNING
                )

    @admin.action(description=_('stop service'))
    def stop_service(self, request, queryset:QuerySet[Service]):
        """ 
        Quista funzione permette di fermare un servizio,
        dal panello di aministrazioine di django.
        """
        control = get_control(app)
        for service in queryset:
            control.revoke(str(service.id), terminate=True)
            service.status = Service.Status.STOP
            service.save()
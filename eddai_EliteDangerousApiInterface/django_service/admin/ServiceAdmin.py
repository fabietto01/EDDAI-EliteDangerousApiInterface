from django.contrib import admin, messages
from django.http.request import HttpRequest
from django.utils.translation import gettext_lazy as _
from django.db.models import QuerySet

from .ReadOnlyServiceEventInline import ReadOnlyServiceEventInline
from ..celey.utility import get_app, get_control

from ..models import Service
from ..form import ServiceForm

app = get_app()

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'name','service',
        'status','args',
        'kwargs','routing_key'
    )
    list_filter = (
        'status', 'routing_key'
    )
    search_fields = (
        'name', 'status',
        'routing_key'
    )
    readonly_fields = (
        'status',
    )
    fieldsets = (
        (
            None, {
                'fields': ('name', 'service', 'status')
            }
        ),
        (
            'Advanced options', {
                'classes': ('collapse',),
                'fields': ('args', 'kwargs', 'routing_key')
            }
        )
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
            try:
                service.status = Service.StatusChoices.STARTING
                service.save()
                self.message_user(
                    request,
                    _('service %(service)s [%(id)s] starting...') % {
                        'service': service.name,
                        'id': service.id
                    },
                    messages.INFO
                )
            except Exception as ex:
                self.message_user(
                    request,
                    _('service %(service)s [%(id)s] error: %(error)s') % {
                        'service': service.name,
                        'id': service.id,
                        'error': ex
                    },
                    messages.ERROR
                )

    @admin.action(description=_('stop service'))
    def stop_service(self, request, queryset:QuerySet[Service]):
        """ 
        Quista funzione permette di fermare un servizio,
        dal panello di aministrazioine di django.
        """
        for service in queryset:
            try:
                service.status = Service.StatusChoices.STOPING
                service.save()
                self.message_user(
                    request,
                    _('service %(service)s [%(id)s] stoping...') % {
                        'service': service.name,
                        'id': service.id
                    },
                    messages.INFO
                )
            except Exception as ex:
                self.message_user(
                    request,
                    _('service %(service)s [%(id)s] error: %(error)s') % {
                        'service': service.name,
                        'id': service.id,
                        'error': ex
                    },
                    messages.ERROR
                )
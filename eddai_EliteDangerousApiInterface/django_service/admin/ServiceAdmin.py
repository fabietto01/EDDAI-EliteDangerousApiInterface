from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from django.db.models import QuerySet

from .ReadOnlyServiceEventInline import ReadOnlyServiceEventInline
from ..celey.utility import get_app

from ..models import Service
from ..form import ServiceForm

app = get_app()

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'task',
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
        'task',
        'status',
        'args',
        'kwargs',
        'routing_key'
    )
    inlines = [ReadOnlyServiceEventInline]
    form = ServiceForm
    actions = [
        'start_service',
        'stop_service'
    ]

    def start_service(self, request, queryset:QuerySet[Service]):
        """
        Quista funzione permette di avviare un servizio,
        dal panello di aministrazioine di django.
        """
        for service in queryset:
            app.send_task(
                service.task,
                args=service.args,
                kwargs=service.kwargs,
                #routing_key=service.routing_key
            )

    def stop_service(self, request, queryset):
        """
        Quista funzione permette di fermare un servizio,
        dal panello di aministrazioine di django.
        """
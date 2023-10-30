from django.contrib import admin

from .ReadOnlyServiceEventInline import ReadOnlyServiceEventInline

from ..models import Service
from ..form import ServiceForm

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
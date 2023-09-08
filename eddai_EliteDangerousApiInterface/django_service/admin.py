from django.contrib import admin

# Register your models here.

from .models import Service, ServiceEvent
from .form import ServiceForm

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
    form = ServiceForm

@admin.register(ServiceEvent)
class EventAdmin(admin.ModelAdmin):
    list_display = (
        'service',
        'event',
        'created',
    )
    list_filter = (
        'service',
        'event',
        'created',
    )
    search_fields = (
        'service',
        'event',
    )
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

#     def all_orders_of_this_customer(self, obj):
#         return format_html(
#  '<a  href="{0}?customer={1}">Orders list of this customer</a>&nbsp;',
#             reverse('admin:customerapp_foodorder_changelist' ), obj.id
#         )

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
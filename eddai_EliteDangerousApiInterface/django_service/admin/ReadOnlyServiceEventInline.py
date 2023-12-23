from django.contrib import admin

from ..models import ServiceEvent

class ReadOnlyServiceEventInline(admin.TabularInline):
    model = ServiceEvent
    extra = 0
    can_delete = False
    max_num = 10
    fields = (
        'event',
        'created',
        'meta'
    )
    readonly_fields = (
        'event',
        'created',
        'meta'
    )

    def has_add_permission(self, request, obj=None):
        """	
        impedisci l'aggiunta di nuovi campi
        """	
        return False 

    def has_change_permission(self, request, obj=None):
        """
        impedisci la modifica dei campi esistenti
        """
        return False  

    def has_delete_permission(self, request, obj=None):
        """
        impedisci la cancellazione dei campi esistenti
        """
        return False
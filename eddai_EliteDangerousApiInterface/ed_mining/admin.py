from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from core.admin import (
    BaseOwnerModelsTabularInline, 
    BaseOwnerModelsModelAdmin
)

from ed_mining.models import *

class RingInline(BaseOwnerModelsTabularInline, admin.TabularInline):
    model = Ring
    raw_id_fields = ("body",)
    readonly_fields = ("created_by", "updated_by", "created_at", "updated_at")
    fields = ("name", "body", "ringType", 'massMT', 'innerRad', 'outerRad', "created_by", "updated_by", "created_at", "updated_at")
    extra = 0
    
class HotSpotInline(BaseOwnerModelsTabularInline, admin.TabularInline):
    model = HotSpot
    raw_id_fields = ("ring",)
    readonly_fields = ("created_by", "updated_by", "created_at", "updated_at")
    fields = ("ring", "type", "count", "created_by", "updated_by", "created_at", "updated_at")
    extra = 0

@admin.register(HotspotType)
class HotspotSignalsAdmin(admin.ModelAdmin):
    model = HotspotType
    list_display = ('name',)
    search_fields = ('name', 'pk', "_eddn")
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        (_('Advanced options'), {
            'fields': ('_eddn',),
            'classes': ('collapse',)
        }),
    )

@admin.register(HotSpot)
class HotSpotAdmin(BaseOwnerModelsModelAdmin, admin.ModelAdmin):
    model = HotSpot
    search_fields = ('ring_name', 'id')
    list_display = ('type', 'ring', 'count',)
    readonly_fields = ("created_at", "updated_at")
    raw_id_fields = ("ring",)
    list_filter = ('type',)
    fieldsets = (
        (None, {
            "fields": ("ring", "type", "count")
        }),
        (_("Advanced options"), {
            "fields": ("created_by", "updated_by", "created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

@admin.register(Ring)
class RingAdmin(BaseOwnerModelsModelAdmin, admin.ModelAdmin):
    model = Ring
    search_fields = ('name', 'body__name', 'id')
    list_display = ('name', 'body', 'ringType', 'massMT', 'innerRad', 'outerRad')
    readonly_fields = ("created_at", "updated_at")
    raw_id_fields = ("body",)
    list_filter = ('ringType',)
    fieldsets = (
        (None, {
            "fields": ("name", "body", "ringType", 'massMT', ('innerRad', 'outerRad'))
        }),
        (_("Advanced options"), {
            "fields": ("created_by", "updated_by", "created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
    inlines = [HotSpotInline]
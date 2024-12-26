from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Register your models here.

from ed_mining.models import *

class RingInline(admin.TabularInline):
    model = Ring
    raw_id_fields = ("body",)
    readonly_fields = ("created_by", "updated_by", "created_at", "updated_at")
    fields = ("name", "body", "ringType", 'massMT', 'innerRad', 'outerRad', "created_by", "updated_by", "created_at", "updated_at")
    extra = 0

    def save_model(self, request, obj, form, change) -> None:
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        return super().save_model(request, obj, form, change)
    
class HotSpotInline(admin.TabularInline):
    model = HotSpot
    raw_id_fields = ("ring",)
    readonly_fields = ("created_by", "updated_by", "created_at", "updated_at")
    fields = ("ring", "type", "count", "created_by", "updated_by", "created_at", "updated_at")
    extra = 0

    def save_model(self, request, obj, form, change) -> None:
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        return super().save_model(request, obj, form, change)

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
class HotSpotAdmin(admin.ModelAdmin):
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

    def get_form(self, request, obj, change, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        if not obj:
            form.base_fields['created_by'].initial = request.user
            form.base_fields['updated_by'].initial = request.user
        else:
            form.base_fields['updated_by'].initial = request.user
        return form 

    def save_model(self, request, obj, form, change) -> None:
        if not obj.pk and not obj.created_by:
            obj.created_by = request.user
        if not obj.updated_by:
            obj.updated_by = request.user
        return super().save_model(request, obj, form, change)

@admin.register(Ring)
class RingAdmin(admin.ModelAdmin):
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

    def get_form(self, request, obj, change, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        if not obj:
            form.base_fields['created_by'].initial = request.user
            form.base_fields['updated_by'].initial = request.user
        else:
            form.base_fields['updated_by'].initial = request.user
        return form 

    def save_model(self, request, obj, form, change) -> None:
        if not obj.pk and not obj.created_by:
            obj.created_by = request.user
        if not obj.updated_by:
            obj.updated_by = request.user
        return super().save_model(request, obj, form, change)
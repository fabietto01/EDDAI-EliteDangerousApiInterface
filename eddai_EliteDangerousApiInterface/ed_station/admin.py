from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Register your models here.

from ed_station.models import *
from ed_economy.admin import CommodityInStationTabularInline

class ServiceInStationTabularInline(admin.TabularInline):
    model = ServiceInStation
    raw_id_fields = ("station",)
    readonly_fields = ("created_by", "updated_by", "created_at", "updated_at")
    fields = ("station", "service", "created_by", "updated_by", "created_at", "updated_at")
    extra = 0

    def save_model(self, request, obj, form, change) -> None:
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        return super().save_model(request, obj, form, change)
    
class StationTabularInline(admin.TabularInline):
    model = Station
    raw_id_fields = ("system",)
    readonly_fields = ("created_by", "updated_by", "created_at", "updated_at")
    fields = ("name", "system", "type", "landingPad", "minorFaction", "distance", "created_by", "updated_by", "created_at", "updated_at")
    extra = 0

    def save_model(self, request, obj, form, change) -> None:
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        return super().save_model(request, obj, form, change)

@admin.register(StationType)
class StationTypeModelAdmin(admin.ModelAdmin):
    model = StationType
    search_fields = ("name",'pk', "_eddn")
    list_display = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        (_('Advanced options'), {
            'fields': ('description','_eddn',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Service)
class ServiceModelAdmin(admin.ModelAdmin):
    model = Service
    search_fields = ("name",'pk', "_eddn")
    list_display = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        (_('Advanced options'), {
            'fields': ('description','_eddn',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Station)
class StationModelAdmin(admin.ModelAdmin):
    model = Station
    search_fields = ("name", "system__name", "id")
    list_display = ("name", "system", "type", "landingPad", "economy", "minorFaction", "distance")
    readonly_fields = ("created_at", "updated_at")
    raw_id_fields = ("system",)
    list_filter = ("landingPad", "type",)
    fieldsets = (
        (None, {
            "fields": ("name", "system",)
        }),
        (_("Station options"), {
            "fields": ("type", ("primaryEconomy", "secondaryEconomy"), "landingPad", "minorFaction", "distance")
        }),
        (_("Advanced options"), {
            "fields": ("created_by", "updated_by", "created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
    inlines = [ServiceInStationTabularInline, CommodityInStationTabularInline]

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
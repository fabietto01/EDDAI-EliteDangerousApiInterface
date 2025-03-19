from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from core.admin import (
    BaseOwnerModelsTabularInline, 
    BaseOwnerModelsModelAdmin
)

from ed_station.models import *
from ed_economy.admin import CommodityInStationTabularInline

class ServiceInStationTabularInline(BaseOwnerModelsTabularInline, admin.TabularInline):
    model = ServiceInStation
    raw_id_fields = ("station",)
    readonly_fields = ("created_by", "updated_by", "created_at", "updated_at")
    fields = ("station", "service", "created_by", "updated_by", "created_at", "updated_at")
    extra = 0
    
class StationTabularInline(BaseOwnerModelsTabularInline, admin.TabularInline):
    model = Station
    raw_id_fields = ("system",)
    readonly_fields = ("created_by", "updated_by", "created_at", "updated_at")
    fields = ("name", "system", "type", "landingPad", "minorFaction", "distance", "created_by", "updated_by", "created_at", "updated_at")
    extra = 0

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
class StationModelAdmin(BaseOwnerModelsModelAdmin, admin.ModelAdmin):
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
        (
            _("EDDN Information"), {
                "fields": ("markerid",),
                "classes": ("collapse",)
            }
        ),
        (_("Advanced options"), {
            "fields": ("created_by", "updated_by", "created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
    inlines = [ServiceInStationTabularInline, CommodityInStationTabularInline]
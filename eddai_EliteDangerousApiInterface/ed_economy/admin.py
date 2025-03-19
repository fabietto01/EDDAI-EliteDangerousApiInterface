from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from core.admin import (
    BaseOwnerModelsTabularInline, 
    BaseOwnerModelsModelAdmin
)

from .models import Commodity, Economy, CommodityInStation

class CommodityInStationTabularInline(BaseOwnerModelsTabularInline, admin.TabularInline):
    model = CommodityInStation
    raw_id_fields = ("station", "commodity")
    readonly_fields = ("created_by", "updated_by", "created_at", "updated_at")
    fields = ("station", "commodity", "buyPrice", "sellPrice", "inStock", "stockBracket", "demand", "demandBracket", "created_by", "updated_by", "created_at", "updated_at")
    extra = 1

@admin.register(CommodityInStation)
class CommodityInStationAdmin(BaseOwnerModelsModelAdmin, admin.ModelAdmin):
    model = CommodityInStation
    search_fields = ("station__name", "commodity__name", "id")
    list_display = (
        "station", "commodity", "buyPrice", "sellPrice", "inStock", "stockBracket", "demand", "demandBracket"
    )
    readonly_fields = ("created_at", "updated_at")
    raw_id_fields = ("station", "commodity")
    list_filter = ("station", "commodity")
    fieldsets = (
        (None, {
            "fields": ("station", "commodity",)
        }),
        (_("Sell"), {
            "fields": ("sellPrice", "inStock", "stockBracket",)
        }),
        (_("Buy"), {
            "fields": ("buyPrice", "demand", "demandBracket",)
        }),
        (_("Advanced options"), {
            "fields": ("created_by", "updated_by", "created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )    

@admin.register(Commodity)
class CommodityAdmin(admin.ModelAdmin):
    model = Commodity
    list_display = ('name', 'meanPrice')
    search_fields = ('name', 'pk', "_eddn")
    fieldsets = (
        (None, {
            'fields': ('name', 'meanPrice')
        }),
        (_('Advanced options'), {
            'fields': ('description', '_eddn',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Economy)
class EconomyAdmin(admin.ModelAdmin):
    list_display = ('name', )
    search_fields = ('name', 'pk', "_eddn")
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        (_('Advanced options'), {
            'fields': ('description', '_eddn',),
            'classes': ('collapse',)
        }),
    )
from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from typing import Any

# Register your models here.

from .models import Commodity, Economy, CommodityInStation

class CommodityInStationTabularInline(admin.TabularInline):
    model = CommodityInStation
    raw_id_fields = ("station", "commodity")
    readonly_fields = ("created_by", "updated_by", "created_at", "updated_at")
    fields = ("station", "commodity", "buyPrice", "sellPrice", "inStock", "stockBracket", "demand", "demandBracket", "created_by", "updated_by", "created_at", "updated_at")
    extra = 1

    def save_model(self, request, obj, form, change) -> None:
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        return super().save_model(request, obj, form, change)

@admin.register(CommodityInStation)
class CommodityInStationAdmin(admin.ModelAdmin):
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

    def get_form(self, request: Any, obj: Any | None = ..., change: bool = ..., **kwargs: Any) -> Any:
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
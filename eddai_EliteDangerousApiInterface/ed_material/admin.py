from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from core.admin import (
    BaseOwnerModelsTabularInline, 
    BaseOwnerModelsModelAdmin
)

from ed_material.models import *
from ed_material.forms import MaterialInPlanetForm

class MaterialInPlanetInline(BaseOwnerModelsTabularInline, admin.TabularInline):
    form = MaterialInPlanetForm
    model = MaterialInPlanet
    raw_id_fields = ("planet",)
    readonly_fields = ("created_by", "updated_by", "created_at", "updated_at")
    fields = ("planet", "material", "percent", "created_by", "updated_by", "created_at", "updated_at")
    extra = 0

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    model = Material
    list_display = ('name', 'type', 'grade')
    search_fields = ('name', "_eddn", "pk")
    list_filter = ('type', 'grade')
    fieldsets = (
        (None, {
            'fields': ('name', 'type', 'grade')
        }),
        (_('Advanced options'), {
            'fields': ('note', '_eddn',),
            'classes': ('collapse',)
        }),
    )

@admin.register(MaterialInPlanet)
class MaterialInPlanetAdmin(BaseOwnerModelsModelAdmin, admin.ModelAdmin):
    model = MaterialInPlanet
    form = MaterialInPlanetForm
    search_fields = ('planet__name', 'material__name', 'id')
    list_display = ('planet', 'material', 'percent')
    readonly_fields = ("created_at", "updated_at")
    raw_id_fields = ("planet", "material")
    list_filter = ('material',)
    fieldsets = (
        (None, {
            "fields": ("planet", "material", "percent")
        }),
        (_("Advanced options"), {
            "fields": ("created_by", "updated_by", "created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )
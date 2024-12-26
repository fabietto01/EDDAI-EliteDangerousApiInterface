from django.contrib import admin
from django.utils.translation import gettext_lazy as _

# Register your models here.

from ed_material.models import *
from ed_material.forms import MaterialInPlanetForm

class MaterialInPlanetInline(admin.TabularInline):
    form = MaterialInPlanetForm
    model = MaterialInPlanet
    raw_id_fields = ("planet",)
    readonly_fields = ("created_by", "updated_by", "created_at", "updated_at")
    fields = ("planet", "material", "percent", "created_by", "updated_by", "created_at", "updated_at")
    extra = 0

    def save_model(self, request, obj, form, change) -> None:
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        return super().save_model(request, obj, form, change)

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
class MaterialInPlanetAdmin(admin.ModelAdmin):
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
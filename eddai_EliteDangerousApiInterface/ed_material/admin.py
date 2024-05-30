from django.contrib import admin

# Register your models here.

from ed_material.models import *
from ed_material.forms import MaterialInPlanetForm

class MaterialInPlanetInline(admin.TabularInline):
    form = MaterialInPlanetForm
    model = MaterialInPlanet
    raw_id_fields = ("planet",)
    extra = 0

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    model = Material
    list_display = ('name', 'type', 'grade', 'note')
    list_filter = ('type', 'grade')
    search_fields = ('name', 'note')

@admin.register(MaterialInPlanet)
class MaterialInPlanetAdmin(admin.ModelAdmin):
    model = MaterialInPlanet
    list_display = ('material', 'planet', 'percent', 'updated_at', 'created_at')
    search_fields = ('material__name', 'planet__name')
    list_filter = ('material', 'planet')
    raw_id_fields = ("material", "planet")
    form = MaterialInPlanetForm
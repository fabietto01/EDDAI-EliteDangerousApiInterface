from django.contrib import admin

# Register your models here.

from ed_material.models import *

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    model = Material
    list_display = ('name', 'type', 'grade', 'note')
    list_filter = ('type', 'grade')
    search_fields = ('name', 'note')

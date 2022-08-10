from django.contrib import admin

from ed_system.models import System

# Register your models here.


@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    model = System
    search_fields = ("name","pk")
    list_display = ("pk","name")
    list_display_links = ("pk","name")
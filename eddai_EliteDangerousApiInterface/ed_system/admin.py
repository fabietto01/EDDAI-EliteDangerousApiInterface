from django.contrib import admin

from ed_system.models import System

# Register your models here.


@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    model = System
    search_fields = ("name","pk")
    list_display = ("name", "economy","security","population","updated")
    list_display_links = ("name",)
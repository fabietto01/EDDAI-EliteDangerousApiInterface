from django.contrib import admin

from ed_system.models import System
from ed_bgs.models import MinorFactionInSystem
# Register your models here.


class MinorFactionInSystemInline(admin.TabularInline):
    model = MinorFactionInSystem
    raw_id_fields = ("minorFaction",)
    extra = 0

@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    model = System
    raw_id_fields = ("conrollingFaction",)
    search_fields = ("name","pk")
    list_display = ("name", "economy","security","population","updated")
    list_display_links = ("name",)
    inlines = [MinorFactionInSystemInline]
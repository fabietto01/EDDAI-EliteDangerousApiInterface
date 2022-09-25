from django.contrib import admin

from ed_system.models import System
from ed_bgs.admin import MinorFactionInSystemInline, PowerInSystemStackedInline
# Register your models here.


@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    model = System
    raw_id_fields = ("conrollingFaction",)
    search_fields = ("name","pk")
    list_display = ("name", "economy","security","population","updated")
    list_display_links = ("name",)
    inlines = [
        MinorFactionInSystemInline, PowerInSystemStackedInline
    ]
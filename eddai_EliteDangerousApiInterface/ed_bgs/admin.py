from django.contrib import admin

from ed_bgs.models import *
# Register your models here.

@admin.register(Faction)
class FactionAdmin(admin.ModelAdmin):
    model = Faction
    search_fields = ("name","pk")
    list_display = ("name", "description")
    list_display_links = ("name",)

@admin.register(MinorFaction)
class MinorFactionAdmin(admin.ModelAdmin):
    model = MinorFaction
    search_fields = ("name","pk")
    list_display = ("name", "allegiance", "government")
    list_display_links = ("name",)

@admin.register(Government)
class GovernmentAdmin(admin.ModelAdmin):
    model = Government
    search_fields = ("name","pk")
    list_display = ("name", "type")
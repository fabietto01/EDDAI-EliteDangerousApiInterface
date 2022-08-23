from django.contrib import admin

from ed_bgs.models import *
# Register your models here.

class MinorFactionInSystemInline(admin.TabularInline):
    model = MinorFactionInSystem
    raw_id_fields = ("system",)
    extra = 0

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
    inlines = [MinorFactionInSystemInline]

@admin.register(Government)
class GovernmentAdmin(admin.ModelAdmin):
    model = Government
    search_fields = ("name","pk")
    list_display = ("name", "type")

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    model = State
    search_fields = ("name","pk")
    list_display = ("name", "type")
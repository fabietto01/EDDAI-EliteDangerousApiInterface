from django.contrib import admin

from ed_bgs.models import *
from ed_bgs.forms.PowerInSystemModelFrom import PowerInSystemForm
# Register your models here.

class MinorFactionInSystemInline(admin.TabularInline):
    model = MinorFactionInSystem
    raw_id_fields = ("system","minorFaction")
    extra = 0

class StateInMinorFaction(admin.TabularInline):
    model = StateInMinorFaction
    raw_id_fields = ("minorFaction",)
    extra = 0

class PowerInSystemTabularInline(admin.TabularInline):
    model = PowerInSystem
    raw_id_fields = ("system",)
    extra = 0

class PowerInSystemStackedInline(admin.StackedInline):
    model = PowerInSystem
    form = PowerInSystemForm
    raw_id_fields = ("system",)
    extra = 0

@admin.register(MinorFactionInSystem)
class MinorFactionInSystemAdmin(admin.ModelAdmin):
    model = MinorFactionInSystem
    list_display = ('system', 'minorFaction', 'Influence')
    search_fields = ('system__name', 'minorFaction__name')
    inlines = [StateInMinorFaction]
    raw_id_fields = ("system","minorFaction")

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
    list_filter = ('allegiance', 'government')
    inlines = [MinorFactionInSystemInline]

@admin.register(Government)
class GovernmentAdmin(admin.ModelAdmin):
    model = Government
    search_fields = ("name","pk")
    list_display = ("name", "type")
    list_filter = ('type',)

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    model = State
    search_fields = ("name","pk")
    list_display = ("name", "type")
    list_filter = ('type',)

@admin.register(Power)
class PowerAdmin(admin.ModelAdmin):
    model = Power
    search_fields = ("name","pk")
    list_display = ("name", "allegiance", "headquarter")
    list_display_links = ("name",)
    list_filter = ('allegiance',)
    raw_id_fields = ("headquarter",)

@admin.register(PowerState)
class PowerStateAdmin(admin.ModelAdmin):
    model = PowerState
    search_fields = ("name","pk")
    list_display = ("name",)

@admin.register(PowerInSystem)
class PowerInSystemAdmin(admin.ModelAdmin):
    model = PowerInSystem
    form = PowerInSystemForm
    search_fields = ("system__name","powers__name","pk")
    list_display = ("__str__", "state")
    list_display_links = ("__str__",)
    list_filter = ('powers',"state")
    raw_id_fields = ("system",)
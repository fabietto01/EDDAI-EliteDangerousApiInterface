from django.contrib import admin

from ed_bgs.models import *
# Register your models here.

class MinorFactionInSystemTabularInline(admin.TabularInline):
    model = MinorFactionInSystem
    raw_id_fields = ("system","minorFaction")
    extra = 0

class StateInMinorFactionTabularInline(admin.TabularInline):
    model = StateInMinorFaction
    raw_id_fields = ("minorFaction",)
    extra = 0

class PowerInSystemTabularInline(admin.TabularInline):
    model = PowerInSystem
    raw_id_fields = ("system",)
    extra = 0

class PowerInSystemStackedInline(admin.StackedInline):
    model = PowerInSystem
    raw_id_fields = ("system",)
    extra = 0

@admin.register(MinorFactionInSystem)
class MinorFactionInSystemModelAdmin(admin.ModelAdmin):
    model = MinorFactionInSystem
    list_display = ('system', 'minorFaction', 'Influence')
    search_fields = ('system__name', 'minorFaction__name')
    inlines = [StateInMinorFactionTabularInline]
    raw_id_fields = ("system","minorFaction")

@admin.register(Faction)
class FactionModelAdmin(admin.ModelAdmin):
    model = Faction
    search_fields = ("name","pk")
    list_display = ("name", "description")
    list_display_links = ("name",)

@admin.register(MinorFaction)
class MinorFactionModelAdmin(admin.ModelAdmin):
    model = MinorFaction
    search_fields = ("name","pk")
    list_display = ("name", "allegiance", "government")
    list_display_links = ("name",)
    list_filter = ('allegiance', 'government')
    inlines = [MinorFactionInSystemTabularInline]

@admin.register(Government)
class GovernmentModelAdmin(admin.ModelAdmin):
    model = Government
    search_fields = ("name","pk")
    list_display = ("name", "type")
    list_filter = ('type',)

@admin.register(State)
class StateModelAdmin(admin.ModelAdmin):
    model = State
    search_fields = ("name","pk")
    list_display = ("name", "type")
    list_filter = ('type',)

@admin.register(Power)
class PowerModelAdmin(admin.ModelAdmin):
    model = Power
    search_fields = ("name","pk")
    list_display = ("name", "allegiance", "headquarter")
    list_display_links = ("name",)
    list_filter = ('allegiance',)
    raw_id_fields = ("headquarter",)

@admin.register(PowerState)
class PowerStateModelAdmin(admin.ModelAdmin):
    model = PowerState
    search_fields = ("name","pk")
    list_display = ("name",)

@admin.register(PowerInSystem)
class PowerInSystemModelAdmin(admin.ModelAdmin):
    model = PowerInSystem
    search_fields = ("system__name","power__name","pk")
    list_display = ("system", "power", "state")
    list_display_links = ("system", "power")
    list_filter = ('power',"state", "system")
    raw_id_fields = ("system",)
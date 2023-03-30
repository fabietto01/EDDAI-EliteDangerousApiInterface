from django.contrib import admin

# Register your models here.

from ed_station.models import *

class ServiceInStationInline(admin.TabularInline):
    model = ServiceInStation
    raw_id_fields = ("station","service")
    extra = 0

@admin.register(StationType)
class StationTypeAdmin(admin.ModelAdmin):
    model = StationType
    search_fields = ("name",'pk')
    list_display = ('name',)

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    model = Service
    search_fields = ("name",'pk')
    list_display = ('name',)

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    model = Station
    raw_id_fields = ("system","minorFaction")
    search_fields = ("name", 'pk','system__name', 'minorFaction__name')
    list_display = (
        'name','system','type','landingPad',
        'distance','economy','minorFaction'
    )
    list_filter = (
        'landingPad','type','primaryEconomy','secondaryEconomy','service'
    )
    inlines = [ServiceInStationInline]
    
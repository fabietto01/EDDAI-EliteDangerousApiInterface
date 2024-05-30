from django.contrib import admin

# Register your models here.

from ed_station.models import *

class ServiceInStationTabularInline(admin.TabularInline):
    model = ServiceInStation
    raw_id_fields = ("station",)
    extra = 0

@admin.register(StationType)
class StationTypeModelAdmin(admin.ModelAdmin):
    model = StationType
    search_fields = ("name",'pk')
    list_display = ('name',)

@admin.register(Service)
class ServiceModelAdmin(admin.ModelAdmin):
    model = Service
    search_fields = ("name",'pk')
    list_display = ('name',)

@admin.register(Station)
class StationModelAdmin(admin.ModelAdmin):
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
    inlines = [ServiceInStationTabularInline]
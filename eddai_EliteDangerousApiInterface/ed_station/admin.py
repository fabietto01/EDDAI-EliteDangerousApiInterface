from django.contrib import admin

# Register your models here.

from ed_station.models import *

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
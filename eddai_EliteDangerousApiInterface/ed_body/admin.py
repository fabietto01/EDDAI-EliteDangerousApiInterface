from django.contrib import admin

# Register your models here.

from django.contrib import admin

from ed_body.models import *

from ed_mining.admin import RingInline
from ed_material.admin import MaterialInPlanetInline
from ed_exploration.admin import SignalInline, SampleInline


class AtmosphereComponentInPlanetInline(admin.TabularInline):
    model = AtmosphereComponentInPlanet
    raw_id_fields = ("planet",)
    extra = 0

@admin.register(StarLuminosity)
class StarLuminosityAdmin(admin.ModelAdmin):
    model = StarLuminosity
    list_display = ('name', 'note')
    search_fields = ('name', 'pk')

@admin.register(StarType)
class StarTypeAdmin(admin.ModelAdmin):
    model = StarType
    list_display = ('name', 'note')
    search_fields = ('name', 'pk')

@admin.register(Star)
class StarAdmin(admin.ModelAdmin):
    model = Star
    list_display = ('name', 'system', 'distance', "luminosity", "starType", "rotating", "orbiting")
    search_fields = ('name', 'system__name', 'id')
    raw_id_fields = ("system",)
    list_filter = ('luminosity', 'starType', )
    inlines = [RingInline]

@admin.register(Planet)
class PlanetAdmin(admin.ModelAdmin):
    model = Planet
    list_display = ('name', 'system', 'distance', "atmosphereType", "planetType", "terraformState")
    search_fields = ('name', 'system__name', 'id')
    raw_id_fields = ("system",)
    list_filter = ('atmosphereType', 'planetType', 'volcanism', 'terraformState', 'reserveLevel')
    inlines = [
        RingInline, AtmosphereComponentInPlanetInline, 
        MaterialInPlanetInline, SignalInline, SampleInline
    ]

@admin.register(AtmosphereType)
class AtmosphereTypeAdmin(admin.ModelAdmin):
    model = AtmosphereType
    list_display = ('name', 'note')
    search_fields = ('name', 'pk', "_eddn")

@admin.register(PlanetType)
class PlanetTypeAdmin(admin.ModelAdmin):
    model = PlanetType
    list_display = ('name', 'note')
    search_fields = ('name', 'pk',)

@admin.register(AtmosphereComponent)
class AtmosphereComponentAdmin(admin.ModelAdmin):
    model = AtmosphereComponent
    list_display = ('name', 'note')
    search_fields = ('name', 'pk',)

@admin.register(Volcanism)
class VolcanismAdmin(admin.ModelAdmin):
    model = Volcanism
    list_display = ('name', 'note')
    search_fields = ('name', 'pk',)
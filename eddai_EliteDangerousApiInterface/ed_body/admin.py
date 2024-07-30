from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from ed_body.models import *

from ed_mining.admin import RingInline
from ed_material.admin import MaterialInPlanetInline
from ed_exploration.admin import SignalInline, SampleInline


class AtmosphereComponentInPlanetInline(admin.TabularInline):
    model = AtmosphereComponentInPlanet
    raw_id_fields = ("planet",)
    readonly_fields = ("created_by", "updated_by", "created_at", "updated_at")
    fields = ("planet", "atmosphere_component", "percent", "created_by", "updated_by", "created_at", "updated_at")
    extra = 0

    def save_model(self, request, obj, form, change) -> None:
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        return super().save_model(request, obj, form, change)

@admin.register(StarLuminosity)
class StarLuminosityAdmin(admin.ModelAdmin):
    model = StarLuminosity
    list_display = ('name', 'note')
    search_fields = ('name', 'pk')
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        (_('Advanced options'), {
            'fields': ('note',),
            'classes': ('collapse',)
        }),
    )

@admin.register(StarType)
class StarTypeAdmin(admin.ModelAdmin):
    model = StarType
    list_display = ('name', 'note')
    search_fields = ('name', 'pk', "_eddn")
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        (_('Advanced options'), {
            'fields': ('note','_eddn'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Star)
class StarAdmin(admin.ModelAdmin):
    model = Star
    search_fields = ('name', 'system__name', 'id')
    list_display = ('name', 'system', 'distance', "luminosity", "starType", "rotating", "orbiting")
    readonly_fields = ("created_at", "updated_at")
    raw_id_fields = ("system","created_by", "updated_by",)
    list_filter = ('luminosity', 'starType', )
    fieldsets = (
        (None, {
            'fields': ('name', 'system', 'bodyID')
        }),
        (_('Stay properties'), {
            'fields': ('absoluteMagnitude', 'age', 'luminosity', 'starType', 'stellarMass', 'subclass',),
            'classes': ('extrapretty',)
        }),
        (_('Optional properties'), {
            'fields':('parentsID', 'distance', 'radius', )
        }),
        (_('Orbital properties'), {
            'fields': ('eccentricity', 'orbitalInclination', 'orbitalPeriod', 'periapsis', 'semiMajorAxis', "ascendingNode", "meanAnomaly"),
            'classes': ('collapse',)
        }),
        (_('Rotation parameters'), {
            'fields':('axialTilt', 'rotationPeriod'),
            'classes':('collapse',)
        }),
        (_('Advanced options'), {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [RingInline]

    def get_form(self, request, obj, change, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        if not obj:
            form.base_fields['created_by'].initial = request.user
            form.base_fields['updated_by'].initial = request.user
        else:
            form.base_fields['updated_by'].initial = request.user
        return form

    def save_model(self, request, obj, form, change) -> None:
        if not obj.pk and not obj.created_by:
            obj.created_by = request.user
        if not obj.updated_by:
            obj.updated_by = request.user
        return super().save_model(request, obj, form, change)

@admin.register(Planet)
class PlanetAdmin(admin.ModelAdmin):
    model = Planet
    search_fields = ('name', 'system__name', 'id')
    list_display = ('name', 'system', 'distance', "atmosphereType", "planetType", "terraformState")
    readonly_fields = ("created_at", "updated_at")
    raw_id_fields = ("system","created_by", "updated_by",)
    list_filter = ('atmosphereType', 'planetType', 'volcanism', 'terraformState', 'reserveLevel')
    fieldsets = (
        (None, {
            'fields': ('name', 'system', 'bodyID')
        }),
        (_('Planet properties'), {
            'fields': (
                'atmosphereType', 'planetType', 'volcanism', 'terraformState', '_compositionIce', '_compositionRock',
                '_compositionMetal', 'landable', 'massEM', 'surfaceGravity', 'surfacePressure', 'tidalLock', 'reserveLevel'
            ),
            'classes': ('extrapretty',)
        }),
        (_('Optional properties'), {
            'fields':('parentsID', 'distance', 'radius', )
        }),
        (_('Orbital properties'), {
            'fields': ('eccentricity', 'orbitalInclination', 'orbitalPeriod', 'periapsis', 'semiMajorAxis', "ascendingNode", "meanAnomaly"),
            'classes': ('collapse',)
        }),
        (_('Rotation parameters'), {
            'fields':('axialTilt', 'rotationPeriod'),
            'classes':('collapse',)
        }),
        (_('Advanced options'), {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    inlines = [
        RingInline, AtmosphereComponentInPlanetInline, 
        MaterialInPlanetInline, SignalInline, SampleInline
    ]

    def get_form(self, request, obj, change, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        if not obj:
            form.base_fields['created_by'].initial = request.user
            form.base_fields['updated_by'].initial = request.user
        else:
            form.base_fields['updated_by'].initial = request.user
        return form 

    def save_model(self, request, obj, form, change) -> None:
        if not obj.pk and not obj.created_by:
            obj.created_by = request.user
        if not obj.updated_by:
            obj.updated_by = request.user
        return super().save_model(request, obj, form, change)

@admin.register(AtmosphereType)
class AtmosphereTypeAdmin(admin.ModelAdmin):
    model = AtmosphereType
    list_display = ('name', 'note')
    search_fields = ('name', 'pk', "_eddn")
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        (_('Advanced options'), {
            'fields': ('note', '_eddn'),
            'classes': ('collapse',)
        }),
    )

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
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        (_('Advanced options'), {
            'fields': ('note',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Volcanism)
class VolcanismAdmin(admin.ModelAdmin):
    model = Volcanism
    list_display = ('name', 'note')
    search_fields = ('name', 'pk', "_eddn")
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        (_('Advanced options'), {
            'fields': ('note', '_eddn'),
            'classes': ('collapse',)
        }),
    )
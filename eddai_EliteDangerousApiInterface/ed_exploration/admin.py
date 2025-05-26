from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from core.admin import (
    BaseOwnerModelsTabularInline, 
    BaseOwnerModelsModelAdmin
)

from ed_exploration.models import *

class SignalInline(BaseOwnerModelsTabularInline, admin.TabularInline):
    model = Signal
    raw_id_fields = ("planet",)
    readonly_fields = ("created_by", "updated_by", "created_at", "updated_at")
    fields = ("planet", "type", "count", "created_by", "updated_by", "created_at", "updated_at")
    extra = 0

class SampleInline(admin.TabularInline):
    model = Sample
    raw_id_fields = ("planet",)
    readonly_fields = ("created_by", "updated_by", "created_at", "updated_at")
    fields = ("planet", "type", "created_by", "updated_by", "created_at", "updated_at")
    extra = 0

@admin.register(SignalSignals)
class SignalsSignalsAdmin(admin.ModelAdmin):
    model = SignalSignals
    list_display = ('name',)
    search_fields = ('name', 'pk', "_eddn")
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        (_('Advanced options'), {
            'fields': ('_eddn',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Signal)
class SignalsAdmin(BaseOwnerModelsModelAdmin, admin.ModelAdmin):
    model = Signal
    search_fields = ('planet__name', 'pk', 'type__name')
    list_display = ('planet', 'type', 'count')
    readonly_fields = ("created_at", "updated_at")
    raw_id_fields = ("planet",)
    list_filter = ('type',)
    fieldsets = (
        (None, {
            'fields': ('planet', 'type', 'count')
        }),
        (_('Advanced options'), {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(SampleSignals)
class SampleSignalsAdmin(admin.ModelAdmin):
    model = SampleSignals
    list_display = ('name',)
    search_fields = ('name', 'pk', "_eddn")
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        (_('Advanced options'), {
            'fields': ('_eddn',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Sample)
class SampleAdmin(BaseOwnerModelsModelAdmin, admin.ModelAdmin):
    model = Sample
    search_fields = ('planet__name', 'pk', 'type__name')
    list_display = ('planet', 'type')
    readonly_fields = ("created_at", "updated_at")
    raw_id_fields = ("planet",)
    list_filter = ('type',)
    fieldsets = (
        (None, {
            'fields': ('planet', 'type')
        }),
        (_('Advanced options'), {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
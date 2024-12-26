from django.contrib import admin
from django.utils.translation import gettext_lazy as _


# Register your models here.

from django.contrib import admin

from ed_exploration.models import *
# Register your models here.

class SignalInline(admin.TabularInline):
    model = Signal
    raw_id_fields = ("planet",)
    readonly_fields = ("created_by", "updated_by", "created_at", "updated_at")
    fields = ("planet", "type", "count", "created_by", "updated_by", "created_at", "updated_at")
    extra = 0

    def save_model(self, request, obj, form, change) -> None:
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        return super().save_model(request, obj, form, change)

class SampleInline(admin.TabularInline):
    model = Sample
    raw_id_fields = ("planet",)
    readonly_fields = ("created_by", "updated_by", "created_at", "updated_at")
    fields = ("planet", "type", "created_by", "updated_by", "created_at", "updated_at")
    extra = 0

    def save_model(self, request, obj, form, change) -> None:
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        return super().save_model(request, obj, form, change)

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
class SignalsAdmin(admin.ModelAdmin):
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
class SampleAdmin(admin.ModelAdmin):
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
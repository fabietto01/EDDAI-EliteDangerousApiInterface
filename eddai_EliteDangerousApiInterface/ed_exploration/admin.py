from django.contrib import admin

from ed_exploration.models import *
# Register your models here.

class SignalInline(admin.TabularInline):
    model = Signal
    raw_id_fields = ("planet",)
    extra = 0

class SampleInline(admin.TabularInline):
    model = Sample
    raw_id_fields = ("planet",)
    extra = 0

@admin.register(SignalSignals)
class SignalsSignalsAdmin(admin.ModelAdmin):
    model = SignalSignals
    list_display = ('name',)
    search_fields = ('name', 'pk',)

@admin.register(Signal)
class SignalsAdmin(admin.ModelAdmin):
    model = Signal
    list_display = ('planet','type')
    raw_id_fields = ("planet",)
    search_fields = ('planet__name', 'pk', 'type__name')
    list_filter = ('type',)

@admin.register(SampleSignals)
class SampleSignalsAdmin(admin.ModelAdmin):
    model = SampleSignals
    list_display = ('name',)
    search_fields = ('name', 'pk',)

@admin.register(Sample)
class SampleAdmin(admin.ModelAdmin):
    model = Sample
    list_display = ('planet','type')
    raw_id_fields = ("planet",)
    search_fields = ('planet__name', 'pk', 'type__name')
    list_filter = ('type',)
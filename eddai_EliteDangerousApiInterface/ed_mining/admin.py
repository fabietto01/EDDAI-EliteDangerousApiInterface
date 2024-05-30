from django.contrib import admin

# Register your models here.

from ed_mining.models import *

class RingInline(admin.TabularInline):
    model = Ring
    raw_id_fields = ("body",)
    extra = 0

@admin.register(HotspotType)
class HotspotSignalsAdmin(admin.ModelAdmin):
    model = HotspotType
    search_fields = ("name","pk")
    list_display = ('name',)

@admin.register(HotSpot)
class HotSpotAdmin(admin.ModelAdmin):
    model = HotSpot
    list_display = ('type','count', 'ring')
    search_fields = ("ring__name","pk")
    list_filter = ('type', )
    raw_id_fields = ("ring",)

@admin.register(Ring)
class RingAdmin(admin.ModelAdmin):
    model = Ring
    list_display = ('name', 'body', "massMT", "ringType", "innerRad", "outerRad")
    search_fields = ('name', 'pk', 'body__name')
    list_filter = ('body', 'ringType')
    raw_id_fields = ("body",)
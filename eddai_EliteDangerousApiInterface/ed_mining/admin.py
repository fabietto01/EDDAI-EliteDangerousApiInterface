from django.contrib import admin

# Register your models here.

from ed_mining.models import *

@admin.register(HotspotSignals)
class HotspotSignalsAdmin(admin.ModelAdmin):
    model = HotspotSignals
    search_fields = ("name","pk")
    list_display = ('name',)

@admin.register(HotSpot)
class HotSpotAdmin(admin.ModelAdmin):
    model = HotSpot
    list_display = ('type','count', 'ring')
    search_fields = ("ring__name","pk")
    list_filter = ('type', )
    raw_id_fields = ("ring",)
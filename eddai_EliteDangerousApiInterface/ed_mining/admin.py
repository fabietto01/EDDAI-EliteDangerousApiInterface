from django.contrib import admin

# Register your models here.

from ed_mining.models import *

@admin.register(HotspotSignals)
class HotspotSignalsAdmin(admin.ModelAdmin):
    model = HotspotSignals
    search_fields = ("name","pk")
    list_display = ('name',)
from django.contrib import admin
from ed_economy.models import *

# Register your models here.

class CommodityInStationInline(admin.TabularInline):
    model = CommodityInStation
    raw_id_fields = ("commodity",'station')
    extra = 0


@admin.register(Economy)
class EconomyAdmin(admin.ModelAdmin):
    model = Economy
    search_fields = ("name","pk")
    list_display = ('name', 'description')

@admin.register(Commodity)
class CommodityAdmin(admin.ModelAdmin):
    model = Commodity
    search_fields = ("name","pk")
    list_display = ('name', 'description')
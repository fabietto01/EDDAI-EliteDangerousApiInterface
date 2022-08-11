from django.contrib import admin
from ed_economy.models import Economy

# Register your models here.



@admin.register(Economy)
class EconomyAdmin(admin.ModelAdmin):
    model = Economy
    search_fields = ("name","pk")
    list_display = ('name', 'description')

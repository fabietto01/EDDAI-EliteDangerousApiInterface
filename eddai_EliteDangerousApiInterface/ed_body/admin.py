from django.contrib import admin

from ed_body.models import *

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
    search_fields = ('name', 'system__name', 'pk')
    raw_id_fields = ("system",)
    list_filter = ('luminosity', 'starType', )
from django.contrib.gis import admin
from django.utils.translation import gettext_lazy as _

from ed_system.models import System
from ed_system.form import SystemModelForm

from ed_station.admin import StationTabularInline

@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    model = System
    form = SystemModelForm
    search_fields = ("name","pk")
    list_display = ("name", "security","population", "economy", "conrollingFaction", "updated_at", "created_at")
    list_display_links = ("name",)
    readonly_fields = ("created_at", "updated_at")
    raw_id_fields = ("conrollingFaction",)
    list_filter = ("security", "primaryEconomy", "secondaryEconomy")
    fieldsets = [
        (None, {
            "fields": (
                "name",
                ("coordinate"),
                "population",
                "security",
                ("primaryEconomy", "secondaryEconomy"),
                "conrollingFaction",
            )
        }),
        (_("Advanced options"), {
            "classes": ("collapse",),
            "fields": ("description","created_by", "updated_by", "created_at", "updated_at")
        })
    ]
    inlines = [StationTabularInline]

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
    
    
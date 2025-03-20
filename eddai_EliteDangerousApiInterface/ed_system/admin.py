from django.contrib.gis import admin
from django.utils.translation import gettext_lazy as _
from core.admin import BaseOwnerModelsModelAdmin

from ed_system.models import System
from ed_system.form import SystemModelForm

from ed_station.admin import StationTabularInline

@admin.register(System)
class SystemAdmin(BaseOwnerModelsModelAdmin, admin.ModelAdmin):
    model = System
    form = SystemModelForm
    search_fields = ("name","pk", "address")
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
        (
            _("EDDN Information"), {
                "fields": ("address",),
                "classes": ("collapse",)
            }
        ),
        (_("Advanced options"), {
            "classes": ("collapse",),
            "fields": ("description","created_by", "updated_by", "created_at", "updated_at")
        })
    ]
    inlines = [StationTabularInline]
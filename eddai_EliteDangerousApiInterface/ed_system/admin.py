from django.contrib import admin

from ed_system.models import System

@admin.register(System)
class SystemAdmin(admin.ModelAdmin):
    model = System
    search_fields = ("name","pk")
    list_display = ("name", "security","population","updated_at", "created_at")
    list_display_links = ("name",)
    fieldsets = [
        (
            None,
            {
                "fields": (
                    "name",
                    ("x", "y", "z"),
                    "population",
                    "security",
                    ("primaryEconomy", "secondaryEconomy"),
                    "conrollingFaction",
                    "description",
                )
            }
        )
    ]


    def save_model(self, request, obj, form, change) -> None:
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        return super().save_model(request, obj, form, change)
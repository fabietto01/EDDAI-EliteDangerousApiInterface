from django.contrib import admin

from eddn.models import DataLog

@admin.register(DataLog)
class DataLogModelAdmin(admin.ModelAdmin):
    model = DataLog
    search_fields = ("schema","error")
    list_display = ("schema", "error", "update", "creat_at")
    list_display_links = ("schema",)
    readonly_fields = ("creat_at", "update", "error")
    list_filter = ("schema","error")
    fieldsets = [
        (None, {
            "fields": (
                "schema",
                "data",
                "error",
            )
        }),
        ("Date", {
            "fields": ("creat_at", "update")
        })
    ]

from django.contrib import admin

from ed_bgs.models import *
# Register your models here.

class MinorFactionInSystemTabularInline(admin.TabularInline):
    model = MinorFactionInSystem
    raw_id_fields = ("system","minorFaction")
    readonly_fields = ("created_by", "updated_by", "created_at", "updated_at")
    fields = ("system", "minorFaction", "Influence", "created_by", "updated_by", "created_at", "updated_at")
    extra = 0
    
    def save_model(self, request, obj, form, change) -> None:
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        return super().save_model(request, obj, form, change)

class StateInMinorFactionTabularInline(admin.TabularInline):
    model = StateInMinorFaction
    raw_id_fields = ("minorFaction",)
    readonly_fields = ("created_by", "updated_by", "created_at", "updated_at")
    fields = ("minorFaction", "state", "phase", "created_by", "updated_by", "created_at", "updated_at")
    extra = 0

    def save_model(self, request, obj, form, change) -> None:
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        return super().save_model(request, obj, form, change)

class PowerInSystemTabularInline(admin.TabularInline):
    model = PowerInSystem
    raw_id_fields = ("system",)
    readonly_fields = ("created_by", "updated_by", "created_at", "updated_at")
    fields = ("system", "power", "state", "created_by", "updated_by", "created_at", "updated_at")
    extra = 0

    def save_model(self, request, obj, form, change) -> None:
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        return super().save_model(request, obj, form, change)

class PowerInSystemStackedInline(admin.StackedInline):
    model = PowerInSystem
    raw_id_fields = ("system",)
    readonly_fields = ("created_by", "updated_by", "created_at", "updated_at")
    fields = ("system", "power", "state", "created_by", "updated_by", "created_at", "updated_at")
    extra = 0

    def save_model(self, request, obj, form, change) -> None:
        if not obj.pk:
            obj.created_by = request.user
        obj.updated_by = request.user
        return super().save_model(request, obj, form, change)

@admin.register(MinorFactionInSystem)
class MinorFactionInSystemModelAdmin(admin.ModelAdmin):
    model = MinorFactionInSystem
    list_display = ('system', 'minorFaction', 'Influence')
    search_fields = ('system__name', 'minorFaction__name')
    raw_id_fields = ("system","minorFaction", "created_by", "updated_by",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = [
        (
            None,
            {
                "fields": 
                    ("system", "minorFaction", "Influence")
            }
        ),
        (
            "Advanced options",
            {
                "classes": ("collapse",),
                "fields": ("created_by", "updated_by", "created_at", "updated_at")
            }
        )
    ]
    inlines = [StateInMinorFactionTabularInline]
    
    def get_form(self, request, obj, change, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        if not obj:
            form.base_fields['created_by'].initial = request.user
            form.base_fields['updated_by'].initial = request.user
        if obj and not obj.updated_by:
            form.base_fields['updated_by'].initial = request.user
        return form

    def save_model(self, request, obj, form, change) -> None:
        if not obj.pk and not obj.created_by:
            obj.created_by = request.user
        if not obj.updated_by:
            obj.updated_by = request.user
        return super().save_model(request, obj, form, change)

@admin.register(Faction)
class FactionModelAdmin(admin.ModelAdmin):
    model = Faction
    search_fields = ("name","pk")
    list_display = ("name", "description")
    list_display_links = ("name",)
    fieldsets = [
        (
            None,
            {
                "fields": (
                    "name",
                    
                )
            }
        ),
        (
            "eddn options",
            {
                "classes": ("collapse",),
                "fields": ("_eddn","description",)
            }
        )
    ]

@admin.register(MinorFaction)
class MinorFactionModelAdmin(admin.ModelAdmin):
    model = MinorFaction
    search_fields = ("name","pk")
    list_display = ("name", "allegiance", "government")
    list_display_links = ("name",)
    list_filter = ('allegiance', 'government')
    readonly_fields = ("created_at", "updated_at")
    fieldsets = [
        (
            None,
            {
                "fields": (
                    "name",
                    "allegiance",
                    "government",
                )
            }
        ),
        (
            "options",
            {
                "classes": ("collapse",),
                "fields": ("description","created_by", "updated_by", ("created_at", "updated_at"))
            }
        )
    ]
    inlines = [MinorFactionInSystemTabularInline]

    def get_form(self, request, obj, change, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        if not obj:
            form.base_fields['created_by'].initial = request.user
            form.base_fields['updated_by'].initial = request.user
        if obj and not obj.updated_by:
            form.base_fields['updated_by'].initial = request.user
        return form

    def save_model(self, request, obj, form, change) -> None:
        if not obj.pk and not obj.created_by:
            obj.created_by = request.user
        if not obj.updated_by:
            obj.updated_by = request.user
        return super().save_model(request, obj, form, change)

@admin.register(Government)
class GovernmentModelAdmin(admin.ModelAdmin):
    model = Government
    search_fields = ("name","pk")
    list_display = ("name", "type")
    list_filter = ('type',)
    fieldsets = [
        (
            None,
            {
                "fields": (
                    "name",
                    "type",
                    "description",
                )
            }
        ),
        (
            "eddn options",
            {
                "classes": ("collapse",),
                "fields": ("_eddn",)
            }
        )
    ]

@admin.register(State)
class StateModelAdmin(admin.ModelAdmin):
    model = State
    search_fields = ("name","pk")
    list_display = ("name", "type")
    list_filter = ('type',)
    fieldsets = [
        (
            None,
            {
                "fields": (
                    "name",
                    "type",
                    "description",
                )
            }
        ),
        (
            "eddn options",
            {
                "classes": ("collapse",),
                "fields": ("_eddn",)
            }
        )
    ]

@admin.register(Power)
class PowerModelAdmin(admin.ModelAdmin):
    model = Power
    search_fields = ("name","pk")
    list_display = ("name", "allegiance", "headquarter")
    list_display_links = ("name",)
    list_filter = ('allegiance',)
    raw_id_fields = ("headquarter",)
    fieldsets = [
        (
            None,
            {
                "fields": (
                    "name",
                    "allegiance",
                    "headquarter",
                )
            }
        ),
        (
            "options",
            {
                "classes": ("collapse",),
                "fields": ("note",)
            }
        )
    ]

@admin.register(PowerState)
class PowerStateModelAdmin(admin.ModelAdmin):
    model = PowerState
    search_fields = ("name","pk")
    list_display = ("name",)
    fieldsets = [
        (
            None,
            {
                "fields": (
                    "name",
                    "description",
                )
            }
        ),
        (
            "eddn options",
            {
                "classes": ("collapse",),
                "fields": ("_eddn",)
            }
        )
    ]

@admin.register(PowerInSystem)
class PowerInSystemModelAdmin(admin.ModelAdmin):
    model = PowerInSystem
    search_fields = ("system__name","power__name","pk")
    list_display = ("system", "power", "state")
    list_display_links = ("system", "power")
    raw_id_fields = ("system","power",)
    readonly_fields = ("created_at", "updated_at")
    fieldsets = [
        (
            None,
            {
                "fields": (
                    "system",
                    "power",
                    "state",
                )
            }
        ),
        (
            "Advanced options",
            {
                "classes": ("collapse",),
                "fields": ("created_by", "updated_by", ("created_at", "updated_at"))
            }
        )
    ]

    def get_form(self, request, obj, change, **kwargs):
        form = super().get_form(request, obj, change, **kwargs)
        if not obj:
            form.base_fields['created_by'].initial = request.user
            form.base_fields['updated_by'].initial = request.user
        if obj and not obj.updated_by:
            form.base_fields['updated_by'].initial = request.user
        return form

    def save_model(self, request, obj, form, change) -> None:
        if not obj.pk and not obj.created_by:
            obj.created_by = request.user
        if not obj.updated_by:
            obj.updated_by = request.user
        return super().save_model(request, obj, form, change)
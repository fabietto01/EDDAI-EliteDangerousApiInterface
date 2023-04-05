from django.contrib import admin
from django_filters.filters import EMPTY_VALUES
from django.utils.translation import gettext_lazy as _
    
class EventFilter(admin.SimpleListFilter):
    
    title = _('event')
    parameter_name = 'event'

    def lookups(self, request, model_admin):
        return (
            ('FSDJump', 'FSDJump'),
            ('Scan', 'Scan'),
            ('SAASignalsFound', 'SAASignalsFound'),
            ('Docked', 'Docked'),
        )

    def queryset(self, request, queryset):
        if not self.value() in EMPTY_VALUES:
            return queryset.filter(
                data__message__event=self.value()
            )
        return queryset
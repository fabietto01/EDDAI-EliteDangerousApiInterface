from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _

from eddn.filters.eventFilter import EventFilter

# Register your models here.
from eddn.models import *

from eddn.service.dataAnalytics.utility import star_analytic

@admin.register(DataLog)
class DataLogAdmin(admin.ModelAdmin):
    model = DataLog
    list_display = ('schema', 'error','update')
    readonly_fields = ('data', 'schema', 'error', 'update')
    actions = ('re_processing',)
    list_filter = (
        'schema', EventFilter
    )

    @admin.action(description=_('data re-processing'))
    def re_processing(self, request, queryset):
        successful = []
        unsuccessful = []
        for instance in list(queryset):
            instance = star_analytic(instance)
            if instance.error:
                unsuccessful.append(instance.pk)
            else:
                successful.append(instance.pk)
        if successful:
            queryset.filter(pk__in=successful).delete()
            self.message_user(
                request,
                _('successful re-processing of %(count)d data') % {
                    'count': len(successful)
                },
                messages.SUCCESS
            )
        if unsuccessful:
            self.message_user(
                request,
                _('unsuccessful re-processing of %(count)d data') % {
                    'count': len(unsuccessful)
                },
                messages.ERROR
            )
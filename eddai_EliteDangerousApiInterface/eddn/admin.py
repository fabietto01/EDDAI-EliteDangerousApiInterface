from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _

from logging import getLogger

from celery import group
from celery.result import GroupResult

from eddn.models import DataLog
from eddn.service.dataAnalytics.utility import star_analytic

log = getLogger("django")

@admin.register(DataLog)
class DataLogModelAdmin(admin.ModelAdmin):
    model = DataLog
    search_fields = ("schema","error")
    list_display = ("pk","schema", "error", "update", "creat_at")
    list_display_links = ("pk", "schema")
    readonly_fields = ("creat_at", "update", "error")
    list_filter = (
        ("schema",admin.AllValuesFieldListFilter),  
    )
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
    actions = ['re_processing']

    @admin.action(description=_('data re-processing'))
    def re_processing(self, request, queryset):
        try:
            tasks = [star_analytic.s(instance) for instance in queryset]
            job = group(tasks)
            result:GroupResult = job.apply_async(
                queue="admin"
            )

            result.get()

            successful = [res.result.id for res in result.results if not res.result.error and res.status == 'SUCCESS']
            unsuccessful = [res.result.id for res in result.results if res.result.error or res.status == 'FAILURE']
            pending = [res.result.id for res in result.results if res.status == 'PENDING']

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
            if pending:
                self.message_user(
                    request,
                    _('pending re-processing of %(count)d data') % {
                        'count': len(pending)
                    },
                    messages.WARNING
                )
        except Exception as e:
            log.error("Error in the re_processing function", exc_info=e)
            self.message_user(
                request,
                _('error in the re-processing of data'),
                messages.ERROR
            )
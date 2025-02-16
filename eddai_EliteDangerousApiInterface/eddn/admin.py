from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _

from logging import getLogger

from celery import group
from celery.result import GroupResult

from eddn.models import DataLog
from eddn.service.worker import star_analytic

log = getLogger("django")

@admin.register(DataLog)
class DataLogModelAdmin(admin.ModelAdmin):
    model = DataLog
    search_fields = ("data","error")
    list_display = ("pk", "schema", "error", "updated_at", "created_at")
    list_display_links = ("pk", "schema",)
    readonly_fields = ("schema", "message", "created_at", "updated_at", "error")
    fieldsets = [
        (None, {
            "fields": ("schema","message","error",)
        }),
        (_("Advanced options"), {
                "classes": ("collapse",),
                "fields": ("data",)
        }),
        (_("Date"), {
            "fields": ("created_at", "updated_at")
        })
    ]
    actions = ['run_re_processing_data']

    @admin.action(description=_('This action is used to manually re-process the data'))
    def run_re_processing_data(self, request, queryset):
        try:
            results = self.sed_re_processing_task(queryset)
            successful, unsuccessful, pending = self.get_re_processing_results_task(results)
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
            log.error("Error in the run_re_processing_data function", exc_info=e)
            self.message_user(
                request,
                _('error in the re-processing of data'),
                messages.ERROR
            )

    def sed_re_processing_task(self, queryset):
        job = group(star_analytic.s(instance) for instance in queryset)
        results:GroupResult = job.apply_async(
            queue="admin"
        )
        return results
    
    def get_re_processing_results_task(self, results:GroupResult):
        results.get()
        successful = [res.result.id for res in results.results if not res.result.error and res.status == 'SUCCESS']
        unsuccessful = [res.result.id for res in results.results if res.result.error or res.status == 'FAILURE']
        pending = [res.result.id for res in results.results if res.status == 'PENDING']
        return successful, unsuccessful, pending
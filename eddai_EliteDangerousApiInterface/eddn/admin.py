from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _

import os
from multiprocessing.pool import ThreadPool

# Register your models here.
from eddn.models import *
from eddn.service.dataAnalytics.JournalAnalytics import JournalAnalytic

@admin.register(DataLog)
class DataLogAdmin(admin.ModelAdmin):
    model = DataLog
    list_display = ('schema', 'error','update')
    readonly_fields = ('data', 'schema', 'error', 'update')
    actions = ('re_processing',)

    @admin.action(description=_('data re-processing'))
    def re_processing(self, request, queryset):
        successful = []
        unsuccessful = []
        number_of_workers = os.cpu_count()
        with ThreadPool(number_of_workers) as pool:
            for analytic, instance in pool.imap(self.process, list(queryset)):
                if analytic != None and analytic.errors == {}:
                    successful.append(instance.pk)
                else:
                    unsuccessful.append(instance.pk)
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


    def process(self, instance:DataLog):
        try:
            if instance.data["$schemaRef"] == "https://eddn.edcd.io/schemas/journal/1":
                analytic = JournalAnalytic(instance=instance)
                return  (analytic.analyst(), instance)
        except Exception as e:
            instance.error = {"error": f"{e}"}
            instance.save(force_update=['error'])
            return (None, instance)

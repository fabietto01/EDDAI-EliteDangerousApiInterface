from celery import shared_task, group
from celery.result import GroupResult
from eddn.models import DataLog
from eddn.service.dataAnalytics.utility import star_analytic


@shared_task(name="auto_analytic", bind=False)
def auto_analytic():
    queryset = DataLog.objects.all()

    tasks = [star_analytic.s(instance) for instance in queryset]
    job = group(tasks)
    result:GroupResult = job.apply_async()

    successful = [res.id for res in result.results if not res.result.error]

    if successful:
        queryset.filter(pk__in=successful).delete()
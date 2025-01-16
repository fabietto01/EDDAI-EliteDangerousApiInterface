from celery import shared_task, group
from celery.result import GroupResult
from eddn.models import DataLog
from eddn.service.dataAnalytics.utility import star_analytic
from django.core.paginator import Paginator

@shared_task(name="auto_analytic", bind=False)
def auto_analytic():
    queryset = DataLog.objects.all().order_by('created_at')
    paginator = Paginator(queryset, 10000)
    for page in paginator.page_range:
        page_obj  = paginator.get_page(page)
        job = group(star_analytic.s(instance) for instance in page_obj )
        result:GroupResult = job.apply_async()
        result.get()
        successful = [res.result.id for res in result.results if not res.result.error and res.status == 'SUCCESS']
        if successful:
            queryset.filter(pk__in=successful).delete()
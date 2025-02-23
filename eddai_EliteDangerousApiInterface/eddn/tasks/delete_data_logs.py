from celery import shared_task

from eddn.models import DataLog

@shared_task(name='delete_data_logs', ignore_result=True)
def delete_data_logs(max_count):
    data_logs = DataLog.objects.filter(_count__gte=max_count).delete()
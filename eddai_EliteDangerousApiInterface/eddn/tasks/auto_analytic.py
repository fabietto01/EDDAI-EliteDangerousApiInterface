from eddai_EliteDangerousApiInterface.celery import app
from celery import group, Task
from celery.result import GroupResult
from eddn.models import DataLog

from eddn.service.worker import star_analytic
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.auth import authenticate
from celery.utils.log import get_task_logger
from users.models import User

class AutoAnalyticTask(Task):
    
    name = 'auto_analytic'
    ignore_result = True
    _agent = None
    log = get_task_logger(__name__)
    _concurrency_limit = 50

    @property
    def agent(self) -> User:
        """
        restituisce l'utente utilizzato per l'analisi, e salva la dai dati
        """
        if not self._agent:
            self._agent = authenticate(
                username=settings.EDDN_USER_NAME_AGENT,
                password=settings.EDDN_USER_PASSWORD_AGENT
            )
        return self._agent

    def get_queryset(self):
        return DataLog.objects.all().order_by('created_at')
    
    def get_paginator(self, queryset, *args, **kwargs) -> Paginator:
        concurrency_limit = kwargs.get('concurrency_limit', self._concurrency_limit)
        orphans = int(concurrency_limit/2)
        return Paginator(queryset, concurrency_limit, orphans=orphans)
    
    def run_tasks(self, page_obj):
        """
        Esegue il task di analisi per ogni istanza di DataLog, se il task ha successo elimina l'istanza
        """
        job = group(star_analytic.s(instance, self.agent) for instance in page_obj)
        result:GroupResult = job.apply_async()
        result.get(propagate=False)
        return [res.result.id for res in result.results if not res.result.error and res.status == 'SUCCESS']
    
    def delete_success_tast(self, queryset, success_tasks:list=None):
        if success_tasks:
            queryset.filter(id__in=success_tasks).delete()

    def run(self, *args, **kwargs):
        """
        Esegue il task di analisi per tutte le istanze di DataLog
        """
        self.log.info(f'started')
        queryset = self.get_queryset()
        paginator = self.get_paginator(queryset, *args, **kwargs)
        self.log.info(f'A total of {paginator.num_pages} pages will be processed')
        for page in paginator.page_range:
            try:
                self.log.info(f'Processing page {page}')
                page_obj  = paginator.get_page(page)
                success_tasks = self.run_tasks(page_obj)
                self.delete_success_tast(queryset, success_tasks)
            except Exception as e:
                self.log.error(f'Error processing page {page}', exc_info=e)
            else:
                self.log.info(f'Page {page} processed')
        self.log.info(f'finished')

app.register_task(AutoAnalyticTask())
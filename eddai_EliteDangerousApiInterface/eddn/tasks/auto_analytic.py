from eddai_EliteDangerousApiInterface.celery import app
from celery import group, Task
from celery.result import GroupResult
from eddn.models import DataLog

from eddn.service.worker import star_analytic
from django.core.paginator import Paginator
from django.conf import settings
from django.contrib.auth import authenticate
from users.models import User

class AutoAnalyticTask(Task):
    
    name = 'auto_analytic'
    ignore_result = True
    _agent = None
    concurrency_limit = 100

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
    
    def get_paginator(self, queryset):
        orphans = int(self.concurrency_limit/2)
        return Paginator(queryset, self.concurrency_limit, orphans=orphans)
    
    def run_tasks(self, page_obj):
        """
        Esegue il task di analisi per ogni istanza di DataLog, se il task ha successo elimina l'istanza
        """
        job = group(star_analytic.s(instance, self.agent) for instance in page_obj)
        result:GroupResult = job.apply_async()
        result.get()
        return [res.result.id for res in result.results if not res.result.error and res.status == 'SUCCESS']
    
    def delete_success_tast(self, queryset, success_tasks:list=None):
        if success_tasks:
            queryset.filter(id__in=success_tasks).delete()

    def run(self):
        """
        Esegue il task di analisi per tutte le istanze di DataLog
        """
        queryset = self.get_queryset()
        paginator = Paginator(queryset, 10000)
        for page in paginator.page_range:
            page_obj  = paginator.get_page(page)
            success_tasks = self.run_tasks(page_obj)
            self.delete_success_tast(queryset, success_tasks)

app.register_task(AutoAnalyticTask())
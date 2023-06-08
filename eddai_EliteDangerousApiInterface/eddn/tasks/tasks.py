from celery import shared_task
from eddn.service.dataAnalytics.utility import star_analytic

@shared_task
def star_analytic_task(istance):
    return star_analytic(istance)
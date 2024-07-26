from django.conf import settings
from eddn.models import DataLog
from eddn.service.dataAnalytics import JournalAnalytic, Commodity3Analytic
from celery import shared_task

@shared_task(name="star_analytic", bind=False)
def star_analytic(istance:DataLog):
    if istance.data["$schemaRef"] == "https://eddn.edcd.io/schemas/journal/1":
        analytic = JournalAnalytic(istance=istance)
        istance = analytic.analyst()
    # elif istance.data["$schemaRef"] == "https://eddn.edcd.io/schemas/commodity/3":
    #     analytic = Commodity3Analytic(istance=istance)
    #     istance = analytic.analyst()
    # elif settings.DEBUG:
    #     istance.error = "Schema not found"
    #     istance.save()
    return istance
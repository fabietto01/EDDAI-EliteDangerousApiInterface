from celery import shared_task
from django.conf import settings
from eddn.models import DataLog

from users.models import User
from .dataAnalysis import JournalAnalysis

@shared_task(name="star_analytic_v2", bind=False)
def star_analytic(istance:DataLog, agent:User, *args, **kwargs) -> DataLog:
    if istance.data["$schemaRef"] == "https://eddn.edcd.io/schemas/journal/1":
        analytic = JournalAnalysis(istance=istance, agent=agent, *args, **kwargs)
        istance = analytic.run_analysis()
    # elif istance.data["$schemaRef"] == "https://eddn.edcd.io/schemas/commodity/3":
    #     analytic = Commodity3Analytic(istance=istance)
    #     istance = analytic.analyst()
    # elif settings.DEBUG:
    #     istance.error = "Schema not found"
    #     istance.save()
    return istance
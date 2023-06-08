from eddn.models import DataLog
from eddn.service.dataAnalytics import JournalAnalytic,  Commodity3Analytic

def star_analytic(istance:DataLog) -> DataLog:
    if istance.data["$schemaRef"] == "https://eddn.edcd.io/schemas/journal/1":
        analytic = JournalAnalytic(istance=istance)
        istance = analytic.analyst()
    elif istance.data["$schemaRef"] == "https://eddn.edcd.io/schemas/commodity/3":
        analytic = Commodity3Analytic(istance=istance)
        istance = analytic.analyst()
    return istance
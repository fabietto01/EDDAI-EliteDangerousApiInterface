from eddn.service.dataAnalytics.BaseDataAnalytics import BaseDataAnalytics
from rest_framework.serializers import Serializer

from eddn.service.seriallizers.commodity.CommodityV3Serializer import CommodityV3Serializer

class Commodity3Analytic(BaseDataAnalytics):

    def get_analyst(self) -> Serializer:
        data = self.get_message()
        return CommodityV3Serializer(data=data)
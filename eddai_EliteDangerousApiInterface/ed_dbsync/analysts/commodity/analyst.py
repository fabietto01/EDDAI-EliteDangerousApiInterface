from ed_dbsync.analysts.base import BaseDataAnalyst

from ed_dbsync.serializers import CommodityV3Serializer

class Commodity3Analyst(BaseDataAnalyst):

    def get_serializer_class(self):
        return CommodityV3Serializer
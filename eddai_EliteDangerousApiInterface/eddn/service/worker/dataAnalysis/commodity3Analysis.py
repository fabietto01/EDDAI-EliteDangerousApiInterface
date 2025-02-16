from .baseDataAnalysis import BaseDataAnalysis
from .errors import NotSerializerError

from ..serializers.commodity import CommodityV3Serializer

class Commodity3Analysis(BaseDataAnalysis):

    def get_serializer_class(self):
        return CommodityV3Serializer
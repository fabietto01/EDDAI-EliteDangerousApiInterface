from ed_core.api.filters.baseDistanceFilterSet import BaseDistanceFilterSet
from ed_body.models import BaseBody

class BaseBodyFilterSet(BaseDistanceFilterSet):
    """
    BaseBodyFilterSet is a filter set class that inherits from BaseDistanceFilterSet.
    It is used to filter BaseBody model instances based on various criteria.
    Attributes:
        distance_fild (str): The field used for distance filtering, set to 'system__coordinate'.
    Meta:
        model (BaseBody): The model class that this filter set is based on.
        fields (dict): A dictionary specifying the fields and their respective lookup types for filtering.
            - 'name': Allows exact match filtering.
            - 'system': Allows exact match filtering.
            - 'distance': Allows filtering with less than ('lt'), less than or equal to ('lte'), greater than ('gt'), and greater than or equal to ('gte') lookups.
    """


    distance_fild = 'system__coordinate'

    class Meta:
        model = BaseBody
        fields = {
            'name': ['exact'],
            'system': ['exact'],
            'distance': ['lt', 'lte', 'gt', 'gte'],
        }
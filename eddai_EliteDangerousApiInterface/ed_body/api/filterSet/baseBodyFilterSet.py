import django_filters
from django.db.models import QuerySet, Case, When, Subquery, IntegerField, OuterRef

from ed_core.api.filters.baseDistanceFilterSet import BaseDistanceFilterSet
from django.utils.translation import gettext_lazy as _

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

    distance_field = 'system__coordinate'
    default_ordering = 'name'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.data.get('system'):
            self.filters.pop('ordering_body', None)
        if self.data.get('system'):
            self.filters.pop('distance_by_system', None)

    def _ordering_body(self, queryset:QuerySet, name, value:bool):
        if value:
            queryset = queryset.annotate(
                _ordering_body=Case(
                    When(parentsID=0, then='bodyID'),
                    default=Subquery(
                        BaseBody.objects.filter(
                            parentsID=OuterRef('bodyID'),
                            system_id=OuterRef('system_id')
                        ).values('bodyID')[:1]
                    ),
                    output_field=IntegerField()
                )
            ).order_by('_ordering_body')
        return queryset

    ordering_body = django_filters.BooleanFilter(
        method='_ordering_body',
        label=_('Order body in system'),
    )

    class Meta:
        model = BaseBody
        fields = {
            'name': ['exact', 'startswith'],
            'system': ['exact'],
            'distance': ['lt', 'lte', 'gt', 'gte'],
        }
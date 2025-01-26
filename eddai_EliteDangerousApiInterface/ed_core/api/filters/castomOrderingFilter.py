import django_filters
from django_filters.constants import EMPTY_VALUES

class OrderingFilterOrDefault(django_filters.OrderingFilter):
    """
    A custom ordering filter that applies a default ordering if no ordering is specified.

    Attributes:
        default_ordering (list): The default ordering to apply if no ordering is specified.

    Methods:
        __init__(*args, **kwargs): Initializes the filter with optional default ordering.
        filter(qs, value): Applies the ordering to the queryset, using default ordering if none is specified.
    """

    def __init__(self, *args, **kwargs):
        self.default_ordering = kwargs.pop('default_ordering', [])
        super().__init__(*args, **kwargs)

    def filter(self, qs, value):
        if value in EMPTY_VALUES and not self.default_ordering in EMPTY_VALUES:
            value = self.default_ordering
        return super().filter(qs, value)
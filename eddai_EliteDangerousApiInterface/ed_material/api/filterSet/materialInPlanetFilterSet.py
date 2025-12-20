import django_filters
from django.utils.translation import gettext_lazy as _

from ed_material.models import MaterialInPlanet, Material

class MaterialInPlanetFilterSet(django_filters.FilterSet):

    material = django_filters.ModelMultipleChoiceFilter(
        queryset=Material.objects.filter(
            type=Material.MaterialType.RAW.value
        ),
        field_name='material',
        label=_('Material'),
        lookup_expr='exact',
    )
    percent_min = django_filters.NumberFilter(
        field_name='percent',
        label=_('Minimum Percent'),
        lookup_expr='gte',
    )
    percent_max = django_filters.NumberFilter(
        field_name='percent',
        label=_('Maximum Percent'),
        lookup_expr='lte',
    )

    class Meta:
        model = MaterialInPlanet
        fields = ['percent', 'material']
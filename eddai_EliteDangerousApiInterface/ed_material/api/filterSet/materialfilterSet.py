import django_filters

from ed_material.models import Material

class MaterialFilterSet(django_filters.FilterSet):

    type = django_filters.TypedMultipleChoiceFilter(
        field_name='type',
        choices=Material.MaterialType.choices,
    )
    grade = django_filters.TypedMultipleChoiceFilter(
        field_name='grade',
        choices=Material.MaterialGrade.choices,
    )

    class Meta:
        model = Material
        fields = ['type', 'grade']
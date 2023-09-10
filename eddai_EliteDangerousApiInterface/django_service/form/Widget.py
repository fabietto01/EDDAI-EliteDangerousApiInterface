from typing import Any
from django.forms.widgets import CheckboxSelectMultiple

class TableSelect(CheckboxSelectMultiple):
    template_name = "django_service/table_select.html"
    option_template_name = "django_service/table_option.html"
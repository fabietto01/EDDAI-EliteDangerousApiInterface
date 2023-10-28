from django.forms.widgets import  CheckboxSelectMultiple

class TableSelect(CheckboxSelectMultiple):
    template_name = "django_service/table_select.html"
    option_template_name = "django_service/table_option.html"

    def __init__(self, fields:list[str]=[], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields = fields

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context["widget"]["fields"] = self.fields
        return context

    
    def render(self, name, value, attrs=None, renderer=None):
        """Render the widget as an HTML string."""
        context = self.get_context(name, value, attrs)
        return self._render(self.template_name, context, renderer)
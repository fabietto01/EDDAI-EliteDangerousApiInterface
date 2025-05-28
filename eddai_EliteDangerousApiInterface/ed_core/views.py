from django.views.generic import TemplateView

# Create your views here.


class IndexTemplateView(TemplateView):
    template_name = 'index.html'
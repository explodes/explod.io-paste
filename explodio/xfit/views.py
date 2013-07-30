from django.views.generic import TemplateView


class XFitView(TemplateView):

    def get_context_data(self, **kwargs):
        pass


class IndexView(XFitView):

    template_name = 'xfit/index.html'

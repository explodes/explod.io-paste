from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView

from explodio.paste import models
from explodio.paste import forms


class IndexView(TemplateView):
    template_name = 'paste/index.html'

    def get_context_data(self, **kwargs):

        ip_address = self.request.META.get('REMOTE_ADDR', None)
        if ip_address:
            ip_pastes = models.Paste.objects.by_ip_address(ip_address)
        else:
            ip_pastes = None

        paste_form = forms.PasteForm(self.request.POST or None)

        return {
            'pastes' : ip_pastes,
            'paste_form' : paste_form
        }

    def post(self, request):

        ctx = self.get_context_data()

        paste_form = ctx['paste_form']

        if paste_form.is_valid():
            pass

        return self.render_to_response(ctx)

class PasteView(TemplateView):
    template_name = 'paste/paste.html'

    def get_context_data(self, **kwargs):
        paste = get_object_or_404(models.Paste, slug=kwargs.get('slug'))
        return {
            'paste' : paste
        }

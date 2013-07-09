from django import http
from django.shortcuts import get_object_or_404
from django.views.generic import View, TemplateView

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
            ip_address = request.META.get('REMOTE_ADDR', '0.0.0.0')
            instance = paste_form.save(ip_address)
            return http.HttpResponseRedirect(instance.get_absolute_url())

        return self.render_to_response(ctx)

class PasteView(TemplateView):
    template_name = 'paste/paste.html'

    def get_context_data(self, **kwargs):

        paste = get_object_or_404(models.Paste, slug=kwargs.get('slug'))
        if paste.expired:
            raise http.Http404

        ip_address = self.request.META.get('REMOTE_ADDR', None)
        if ip_address:
            ip_pastes = models.Paste.objects.by_ip_address(ip_address)
        else:
            ip_pastes = None

        return {
            'paste' : paste,
            'pastes' : ip_pastes
        }

class PasteHtml(View):

    def get(self, request, **kwargs):
         paste = get_object_or_404(models.Paste, slug=kwargs.get('slug'))
         return http.HttpResponse(paste.highlighted)


from django import http
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.urlresolvers import reverse
from django.views.generic import View, TemplateView

from explodio.accounts import forms


class LoginView(TemplateView):

    template_name = 'accounts/login.html'

    def get_context_data(self, **kwargs):
        """
        Provide context to the template
        - login_form (LoginForm)
        :param kwargs: Request **kwargs
        :return: Context dict
        """
        ctx = super(LoginView, self).get_context_data(**kwargs)

        login_form = forms.LoginForm(self.request.POST or None)

        additional = {
            'login_form' : login_form,
        }
        ctx.update(additional)
        return ctx

    def post(self, request, *args, **kwargs):
        """
        Log the user in if they have the credentials
        :return: HttpResponse
        """
        ctx = self.get_context_data(**kwargs)

        login_form = ctx['login_form']

        if login_form.is_valid():

            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.info(request, 'Logged in')
                    next = request.GET.get('next', None)
                    if not next:
                        next = reverse('accounts:login')
                    return http.HttpResponseRedirect(next)
                else:
                    messages.warning(request, 'This account is disabled')
            else:
                messages.error(request, 'Invalid username/password')
        return self.render_to_response(ctx)

class LogoutView(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.info(request, 'Logged out')
        next = request.GET.get('next', request.POST.get('next', None))
        if not next:
            next = reverse('accounts:login')
        return http.HttpResponseRedirect(next)

    def post(self, request, *args, **kwargs):
        return self.get(request, *args, **kwargs)

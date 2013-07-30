from datetime import date

from django import http
from django.views.generic import TemplateView

from explodio.common import iterator
from explodio.xfit import forms
from explodio.xfit import models


class XFitView(TemplateView):
    """
    XFitView helper functions
    """

    def get_gyms(self, user=None):
        """
        Get a list of Gyms for a user.
        :param user: User to get gyms for, pulled from request by default
        :return: Gym QuerySet
        """
        if user is None and self.request.user.is_authenticated():
            user = self.request.user
        q = models.Gym.objects.active()
        if user:
            q = q.for_user(user)
        return q

    def get_wods(self, day=None):
        """
        Gets a list of WorkoutOfTheDay
        :param day: Specific day to get WODs for, defaults to today
        :return: QuerySet of WorkoutOfTheDay
        """
        if day is None:
            day = date.today()
        return models.WorkoutOfTheDay.objects.for_day(day)

    def get_user_wods(self, user=None, day=None):
        """
        Gets UserWODs for a User for a day
        :param user: User to get gyms for, pulled from request by default
        :param day: Specific day to get WODs for, defaults to today
        :return: QuerySet of UserWOD
        """
        if user is None and self.request.user.is_authenticated():
            user = self.request.user
        if day is None:
            day = date.today()
        return models.UserWOD.objects \
            .for_user(user) \
            .for_day(day) \
            .select_related('wod')

    def get_wod_pairs(self, user=None, day=None):
        """
        Returns WODs paired to UserWODs
        :param user: User to get gyms for, pulled from request by default
        :param day: Specific day to get WODs for, defaults to today
        :return: list of (WorkoutOfTheDay, UserWOD or None)
        """
        wods = self.get_wods(day)
        user_wods = self.get_user_wods(user, day)
        pairs = iterator.pair_left(wods, user_wods,
            searcher=lambda wod, uw: uw.wod.id == wod.id)
        return pairs

    def get_wod_forms(self, data, user=None, day=None):
        """
        Build UserWODForms using the given POST data, for a User and day
        :param data: POST data to apply to forms
        :param user: User to get gyms for, pulled from request by default
        :param day: Specific day to get WODs for, defaults to today
        :return: list of UserWODForm
        """
        if user is None and self.request.user.is_authenticated():
            user = self.request.user
        wod_pairs = self.get_wod_pairs(user=user, day=day)

        wod_forms = []

        for index, pair in enumerate(wod_pairs):
            wod, user_wod = pair
            wod_form = forms.UserWODForm(user, wod, user_wod, index, data)
            wod_forms.append(wod_form)

        return wod_forms


class XFitContextView(XFitView):
    """
    XFitView with default context
    """

    def get_context_data(self, **kwargs):
        """
        Supply default context to subclasses of this view.
        - gyms (QuerySet of Gyms)
        :param kwargs: Request **kwargs
        :return: Context dict
        """
        ctx = super(XFitContextView, self).get_context_data(**kwargs)
        additional = {
            'gyms' : self.get_gyms(),
        }
        ctx.update(additional)
        return ctx

class IndexView(XFitContextView):
    """
    The index page.
    """

    template_name = 'xfit/index.html'

    def get_context_data(self, **kwargs):
        """
        Supply context to index.html
        - wod_forms (list of UserWODForm)
        - extra_gyms (gyms that don't have WODs for the given day)
        :param kwargs: Request **kwargs
        :return: Context dict
        """
        ctx = super(IndexView, self).get_context_data(**kwargs)

        gyms = ctx['gyms']

        wod_forms = self.get_wod_forms(self.request.POST or None)
        gyms_with_wods = set((wod_form.wod.gym for wod_form in wod_forms))
        extra_gyms = set(gyms) - set(gyms_with_wods)

        additional = {
            'wod_forms' : wod_forms,
            'extra_gyms' : extra_gyms,
        }
        ctx.update(additional)

        print 'GET CTX DATA'

        return ctx

    def post(self, request, *args, **kwargs):
        """
        Handle POST method.
        :param request: View request
        :param args: View *args
        :param kwargs: View **kwargs
        :return: HttpResponse
        """
        action = request.POST.get('action')

        if action == 'update-wods':
            return self.post_update_wods(request, *args, **kwargs)

        # Unknown action
        return http.HttpResponseBadRequest()

    def post_update_wods(self, request, *args, **kwargs):
        """
        POST UserWODForm data.
        :param request: View request
        :param args: View *args
        :param kwargs: View **kwargs
        :return: HttpResponse
        """
        ctx = self.get_context_data(**kwargs)

        wod_forms = ctx['wod_forms']

        valid = all((wod_form.is_valid() for wod_form in wod_forms))

        if valid:
            for wod_form in wod_forms:
                wod_form.save()

        return self.render_to_response(ctx)


from datetime import date
from django.views.generic import TemplateView

from explodio.common import iterator
from explodio.xfit import forms
from explodio.xfit import models


class XFitView(TemplateView):

    def get_gyms(self):
        return models.Gym.objects.active()

    def get_wods(self, day=None):
        if day is None:
            day = date.today()
        return models.WorkoutOfTheDay.objects.by_day(day)

    def get_user_wods(self, user=None, day=None):
        if user is None and self.request.user.is_authenticated():
            user = self.request.user
        if day is None:
            day = date.today()
        return models.UserWOD.objects \
            .by_user(user) \
            .by_day(day) \
            .select_related('wod')

    def get_wod_pairs(self, user=None, day=None):
        wods = self.get_wods(day)
        user_wods = self.get_user_wods(user, day)
        pairs = iterator.left_outer_join(wods, user_wods,
            searcher=lambda wod, uw: uw.wod.id == wod.id)
        return pairs

    def get_wod_forms(self, data, user=None, day=None):
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

    def get_context_data(self, **kwargs):
        ctx = super(XFitContextView, self).get_context_data(**kwargs)
        additional = {
            'gyms' : self.get_gyms(),
        }
        ctx.update(additional)
        return ctx

class IndexView(XFitContextView):

    template_name = 'xfit/index.html'

    def get_context_data(self, **kwargs):
        ctx = super(IndexView, self).get_context_data(**kwargs)
        additional = {
            'wod_forms' : self.get_wod_forms(self.request.POST or None),
        }
        ctx.update(additional)
        return ctx

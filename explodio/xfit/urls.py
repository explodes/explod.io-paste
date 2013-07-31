from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required

from explodio.xfit import views


urlpatterns = patterns('',
    # The WOD page.
    url(r'^$',
        login_required(views.IndexView.as_view()),
        name='index'),

    # The WOD page stats.
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        login_required(views.IndexView.as_view()),
        name='index'),

    # The comparison page.

    # The gym page.

    # The workout page.

    # The stats page.

    # The graphs page.

    # The gamification page.

    # The high-score page.
)

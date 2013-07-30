from django.conf.urls import patterns, url

from explodio.xfit import views


urlpatterns = patterns('',
    # The WOD page.
    url(r'^$', views.IndexView.as_view(), name='index'),

    # The WOD page stats.
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',
        views.IndexView.as_view(),
        name='index'),

    # The comparison page.

    # The gym page.

    # The workout page.

    # The stats page.

    # The graphs page.

    # The gamification page.

    # The high-score page.
)

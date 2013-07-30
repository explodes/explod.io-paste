from django.conf.urls import patterns, url

from explodio.xfit import views


urlpatterns = patterns('',
    # The home page.
    url(r'^$', views.IndexView.as_view(), name='index'),

    # The comparison page.

    # The gym page.

    # The workout page.

    # The stats page.

    # The graphs page.

    # The gamification page.

    # The high-score page.
)

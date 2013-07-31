from django.conf.urls import patterns, url

from explodio.accounts import views


urlpatterns = patterns('',
    # The login page.
    url(r'^login/$',
        views.LoginView.as_view(),
        name='login'),

    # The logout page.
    url(r'^logout/$',
        views.LogoutView.as_view(),
        name='logout'),

)

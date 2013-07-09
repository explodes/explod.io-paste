from django.conf.urls import patterns, url

from explodio.paste import views


urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<slug>[a-f0-9]+)/$', views.PasteView.as_view(), name='paste'),
    url(r'^(?P<slug>[a-f0-9]+)/html/$', views.PasteHtml.as_view(), name='paste-content'),
)

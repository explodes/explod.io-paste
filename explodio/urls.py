from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('explodio.main.urls', namespace='main')),
    url(r'^paste/', include('explodio.paste.urls', namespace='paste')),
    url(r'^xfit/', include('explodio.xfit.urls', namespace='xfit')),
    url(r'^admin/', include(admin.site.urls)),
)

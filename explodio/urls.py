from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^', include('explodio.main.urls', namespace='explodio:main')),
    url(r'^paste/', include('explodio.paste.urls', namespace='explodio:paste')),
    url(r'^admin/', include(admin.site.urls)),
)

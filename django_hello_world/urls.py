from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'django_hello_world.hello.views.home'),
    url(r'^requests/$', 'django_hello_world.hello.views.requests'),

    url(r'^admin/', include(admin.site.urls)),
)

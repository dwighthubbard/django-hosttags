from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import redirect_to

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hostlists_project.views.home', name='home'),
    # url(r'^hostlists_project/', include('hostlists_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^/$',redirect_to,{'url':'/admin/hosttags/host/'}),
    url(r'^$', redirect_to,{'url':'/admin/hosttags/host/'}),
    (r'^api/', include('api.urls')),
)

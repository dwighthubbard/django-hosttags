from django.conf.urls.defaults import *
from piston.resource import Resource
from hostlists_project.api.handlers import HostHandler

host_handler = Resource(HostHandler)

urlpatterns = patterns('',
   url(r'^host/(?P<tags>[^/]+)/', host_handler),
   url(r'^host/', host_handler),
   url(r'^host?', host_handler),
)

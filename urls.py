from django.conf.urls.defaults import *
#from port_check.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^vp_check_site/', include('vp_check_site.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^port_check/', 'port_check.views.port_check'),
    (r'^user_info/', 'port_check.views.user_info'),
    (r'^port_check_status/', 'port_check.views.port_check_status'),
)

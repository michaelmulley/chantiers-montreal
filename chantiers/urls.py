from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'chantiers.search.views.prototype'),
    (r'^from_line/$', 'chantiers.search.views.points_via_line'),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
)

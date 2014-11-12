from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from logger.views import DeviceViewSet, LogViewSet

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'Logs', LogViewSet)
router.register(r'Devices', DeviceViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browseable API.
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'rest_sample.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include(router.urls)),
    url(r'^', include('logger.urls')),
    url(r'^admin/', include(admin.site.urls)),
)
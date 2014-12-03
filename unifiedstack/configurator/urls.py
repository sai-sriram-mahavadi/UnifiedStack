from django.conf.urls import patterns, url
from configurator import views

urlpatterns = patterns('',
                       url(r'^configurator$', views.configure),
                       url(r'^configurator/api/v1.0/dtl$', views.device_type_list),
                       url(r'^configurator/api/v1.0/dtsl/(?P<p_dtype>[A-Z]+)/$', views.device_type_settings_list),
                       url(r'^configurator/api/v1.0/dlist/$', views.device_list),
                       url(r'^configurator/api/v1.0/dlist$', views.device_list),
                       url(r'^configurator/api/v1.0/dslist/(?P<dpk>[0-9]+)/$', views.device_settings_list),
                       url(r'^configurator/api/v1.0/dslist/(?P<dpk>[0-9]+)$', views.device_settings_list),
                       url(r'^configurator/api/v1.0/configure$', views.configure_setup),
                       
                       url(r'^configurator/sample$', views.sample),
                       url(r'^configurator/serversample$', views.server_binding_sample),
                       url(r'^configuration$', views.server_binding_post),
                )

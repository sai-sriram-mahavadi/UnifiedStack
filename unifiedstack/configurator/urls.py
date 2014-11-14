from django.conf.urls import patterns, url
from configurator import views

urlpatterns = patterns('',
                       url(r'^configurator$', views.configure),
                       url(r'^configurator/sample$', views.sample),
                       url(r'^dslist/(?P<dpk>[0-9]+)/$', views.device_settings_list),
                       url(r'^configurator/serversample$', views.server_binding_sample),
                       url(r'^configuration$', views.server_binding_post),
                )



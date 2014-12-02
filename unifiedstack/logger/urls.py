from django.conf.urls import patterns, url
from logger import views

urlpatterns = patterns('',
                       url(r'^devicelist$', views.device_list),
                       url(r'^devicelist/$', views.device_list),
                       url(r'^devicelist/(?P<pk>[0-9]+)/$', views.device_detail),
                       url(r'^loglist$', views.log_list),
                       url(r'^loglist/$', views.log_list),
                       url(r'^console/$', views.list_n_console_logs),
                       url(r'^loglist/(?P<pk>[0-9]+)/$', views.log_detail),
                       url(r'^sample/$', views.sample),
                      )



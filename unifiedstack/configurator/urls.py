from django.conf.urls import patterns, url
from configurator import views

urlpatterns = patterns('',
                       url(r'^api/configure$', views.configure),
                       url(r'^api/configure$', views.configure),
                      )



from django.conf.urls import patterns
from django.conf.urls import url

from openstack_dashboard.dashboards.unifiedstack.spawnvm import views

urlpatterns = patterns('',
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^index$', views.IndexView.as_view(), name='index'),
    url(r'^calculatesum$', views.ResultView.as_view(), name='calculatesum'),
)
